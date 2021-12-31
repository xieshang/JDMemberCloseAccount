import threading
import requests
import logging
import queue
import time
import os
from requests.adapters import HTTPAdapter

class MulThreadDownload(threading.Thread):
    download_thread_num = 8
    # 文件分段大小，1024*1024即1mb大小
    def __init__(self,download_url,path,filename='',download_thread_num=0,part_size=1024*1024):
        threading.Thread.__init__(self)
        self.download_url = download_url
        self.path=path
        self.file_name=filename
        self.download_thread_num=download_thread_num
        self.part_size=part_size
        self.file=None
        self.threads=[]
        self.lock=threading.Lock()
        # 共用一个session，减少tcp请求的次数
        self.session=requests.session()
        # 使用requests自带的失败重试解决方案
        self.session.mount('http://', HTTPAdapter(max_retries=5))
        self.session.mount('https://', HTTPAdapter(max_retries=5))
        self.file_size=-1
        self.downloaded_size=0
        self.taskQ=queue.Queue()
        self.mbsize=-1
    def download_thread(self,threadid):
        # 当下载任务队列为空时，线程就会退出，停止执行
        while not self.taskQ.empty():
            part_dict=self.taskQ.get(block=True,timeout=None)
            headers={'Range':'bytes={0}-{1}'.format(part_dict['start'],part_dict['end'])}
            # response=requests.get(url=self.download_url,stream=True,headers=headers)
            # 因为分段自动是小文件，所以没必要用慢速下载，直接载入内存就行了
            response=self.session.get(url=self.download_url,headers=headers)
            # with self.lock:
            #     self.file.seek(part_dict['start'])
            #     self.file.write(response.content)
            with self.lock:
                self.file.seek(part_dict['start'])
                self.file.write(response.content)
                self.downloaded_size+=part_dict['end']-part_dict['start']
            logging.debug(str(threadid)+' download succeed: '+str(part_dict))
            # for chunk in response.iter_content(chu)
    def analysis_filename(self):
        # 从url地址中获取文件名
        filename = self.download_url.split('/')[-1]
        logging.debug('analysis filename form url,got{0},from{1}'.format(filename,self.download_url))
        return filename
    def progress_bar_thread(self):
        start_time=int(time.time())
        sleep_time=0.1
        former_size=0
        while self.downloaded_size!=self.file_size:
            # 计算下载速度
            speed = (self.downloaded_size-former_size)*(1/sleep_time)
            speedstr=self.speed_str(speed)
            former_size=self.downloaded_size

            # 计算剩余时间
            remaining_size=self.file_size-self.downloaded_size
            if speed>0:
                remaining_seconds=round(remaining_size/speed,2)
                eta = self.ETA_str(remaining_seconds)
            else:
                eta='???'
            # 计算下载百分比
            percentage=self.downloaded_size/self.file_size*100

            print('\r[downloading]: {:.2f}% of {}mb speed:{} ETA:{}'.format(percentage,self.mbsize,speedstr,eta),end='')
            time.sleep(0.1)
        # 因为一直不换行，所以下载完要换行
        end_time =int(time.time())
        print('\n 100% of {}mb in {}'.format(self.mbsize,self.ETA_str(end_time-start_time)))
    def speed_str(self,speedbytes):
        if speedbytes>1024*1024:
            return str(round(speedbytes/1024/1024,2))+' mb/s'
        elif speedbytes>1024:
            return str(round(speedbytes/1024,2))+' kb/s'
        else:
            return str(speedbytes)+' b/s'
    def ETA_str(self,seconds):
        if seconds>60*60:
            hour=seconds//3600
            min=(seconds-hour*3600)//60
            second=(seconds-hour*3600)%60
            str='{0}h{1}m{2}s'.format(hour,min,second)
        elif seconds>60:
            min = seconds // 60
            second = seconds % 60
            str = '{0}m{1}s'.format(min, second)
        else:
            str='{0}s'.format(seconds)
        return str

    def run(self):
        # 1.从url中获取文件信息，为线程分配下载资源做准备
        # 从url提取文件名
        logging.info('url:'+self.download_url)
        # 从文件响应头获取content-length。以及Accept-Ranges字段为分配下载做准备
        response_head = requests.head(self.download_url)
        if self.file_name == '':
            self.file_name = self.analysis_filename()
        # if not response_head.headers.has_key('Accept-Ranges'):
        if 'Accept-Ranges' not in response_head.headers.keys() :
            logging.fatal("不支持断点续传,不支持多线程下载")
        self.file_size = int(response_head.headers['Content-Length'])
        # 计算文件大小mb值
        self.mbsize=round(self.file_size / 1024 / 1024, 2)
        # 获取文件大小后，创建相同大小的文件
        if self.path=='':
            filepath=self.file_name
        else:
            filepath=os.path.join(self.path,self.file_name)
        self.file = open(filepath, 'wb')
        self.file.truncate(self.file_size)
        # 获得文件大小后划分下载任务。按照part_size进行划分
        # 最终分块任务数为，比如说文件大小为1gb，分块1mb，那么就要分成1024份,如果1gb多一点点，那么1025份
        part_num = self.file_size//self.part_size+1
        # 发送的请求头带上这一条就可以请求指定区间的数据 Range: bytes = 0 - 1048576

        # 创建下载队列，把Range的值字符串进行拼接
        # 这里存在一个小问题，请求0-1024*1024的资源，实际上返回的是1024*1024+1大小的资源，但是在用seek写的过程中，因为多出来的一字节会不断覆盖掉，所以没有问题。
        # 从代码可读性考虑上看，这样其实也好。我们先测试一下这样是否可行再改进

        for num in range(part_num):
            start= num*self.part_size
            end=(num+1)*self.part_size
            if num==part_num-1:
                end=self.file_size
            # rangestr='bytes={0}-{1}'.format(num*self.part_size,endSize)
            part_dict={
                    'partnum':part_num,
                    'start':start,
                       'end':end
            }
            self.taskQ.put(part_dict)
            logging.debug(str(part_dict))
            # print(rangestr)
        # 开启进度条线程
        threading.Thread(target=self.progress_bar_thread,args=()).start()
        for i in range(self.download_thread_num):
            t=threading.Thread(target=self.download_thread,args=(i,))
            self.threads.append(t)
            t.start()
        for t in self.threads:
            t.join()

        # 全部线程运行结束，说明文件下载完成
        self.file.close()


def main():
    # logging.basicConfig(format="%(asctime)s:%(levelname)s:%(message)s",level=logging.DEBUG)
    logging.basicConfig(format="%(asctime)s:%(levelname)s:%(message)s",level=logging.INFO)
    mul=MulThreadDownload(download_url=r'http://www.python.org/ftp/python/3.6.0/python-3.6.0.exe', path='.', filename='python-3.6.0.exe', download_thread_num=1)
    mul.start()
if __name__ == '__main__':
    main()