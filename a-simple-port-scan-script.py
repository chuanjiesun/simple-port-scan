###############这是个判断端口开放的简单脚本#########################
###############如果需要详细的信息，请使用下面使用nmap库扫描的脚本（100行后面）##########
import threading, socket, sys
from time import ctime, time

changgui_port = [21,22,23,25,53,80,81,110,139,161,443,445,513,514,873,1433,1434,1521,3306,
			3389,3690,5432,6000,6001,7001,7071,8008,8080,8088,10050,10051,]
threads = []#把线程实例t组成存储list类型

def scan(port):
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(5)#设置超时时间
		result = sock.connect_ex((Host, port))
	#	print(result)
		if result == 0:
			print('port {} open'.format(port))
		sock.close()
	except Exception as e:
		print(e)
def wanquan():
	for i in range(1,65535,100):#可以将第三个参数作为手动输入的线程数
		k = 65535-i
		if k>100:  #如果剩下不到100个端口，就开启剩下的端口数的线程
			k = 100
		else:
			k = k
		for j in range(k):#开启100个线程
			j = i+j
			t = threading.Thread(target=scan, args=(j,))#如果参数写为args=j就会报错：参数必须为一个序列
			threads.append(t)
#			print(type(threads)) #<Thread(Thread-39, initial)>
		for m in range(len(threads)):
			threads[m].start()
		for n in range(len(threads)):
			threads[n].join()
		threads.clear()#清空进行下一个循环

def changgui():
	len_changgui = len(changgui_port)
	for i in range(0,len_changgui,10):
		k = len_changgui - i
		if k > 10:
			k = 10
		else:
			k = k
		for j in range(k):
			j = i+j
			t = threading.Thread(target=scan, args=(changgui_port[j],))	
			threads.append(t)
		for m in range(len(threads)):
			threads[m].start()
		for n in range(len(threads)):
			threads[n].join()
		threads.clear()

def main():
	if sys.argv[2] == 'cg':#changgui
		print('\n常见端口扫描模式')
		changgui()
	elif sys.argv[2] == 'wq':#wanquan
		print('\n完全端口扫描模式')
		wanquan()

if __name__ == '__main__':
	length_canshu = len(sys.argv)
	if length_canshu == 3:
		try:
			#Host = '192.168.167.2'#ip可以作为输入参数argv[]
			Host = sys.argv[1]
			print('Host is : {}'.format(Host))
			Host = socket.gethostbyname(sys.argv[1])#若果是域名就转换为ip
			print('{0}  <==>  {1}'.format(Host,sys.argv[1]))
			t1 = time()
			print('scan start at : {}'.format(ctime()))
			main()
			print('\nscan stop at : {}'.format(ctime()))
			t2 = time()
			print('端口扫描耗时：{0:.2f} 秒'.format(t2-t1))
		except Exception as e:
			print('哥们，可能网络不行或者输错了！{}'.format(e))
			print('\nUsage: xx.py ip/hostname  cg/wq')
			print('example: xx.py www.baidu.com cg')
			print('cg:常见端口扫描\nwq:完整端口扫描')
	else:
		print('\nUsage: xx.py ip/hostname  cg/wq')
		print('example: xx.py www.baidu.com cg')
		print('cg:常见端口扫描\nwq:完整端口扫描')
		sys.exit()
	#对于time()函数返回float类型，只取两位小数  具体更多用法查format()
	#{:.2f}与{0:.2f}结果一样







		
#######################################nmap版本扫描脚本###########################################
'''
python3.3 py-nmap.py -H 192.168.1.10-20 -p 21-1000 
python3.3 py-nmap.py -H 192.168.1.10-20 -p 21-1000 [--arg="-Pn -sV --open"]
python3.3 py-nmap.py -H 192.168.1.10-20 -p cg [--arg="-Pn -sV --open"]#常见端口扫描,可以自定义端口cg_ports
python3.3 py-nmap.py -H 192.168.1.10-20 -p 21-80,3306  [--arg="-Pn -sV --open"]
python3.3 py-nmap.py -H 192.168.1.10-20,111.123.23.3 -p 21-1000 [--arg="-Pn -sV --open"]

'''
import socket, sys
from nmap import nmap
import argparse
from urllib import request

cg_ports = [21,22,23,25,53,80,81,110,119,139,143,161,443,445,513,514,587,873,1433,1434,1521,3306,3307,3389,3690,5432,6000,6001,7001,7071,8008,8080,8088,10050,10051]

def main():
	parser = argparse.ArgumentParser(description = 'this is a test message', 
	usage=''' %(prog)s [options]\
		\nyou need tpo specify a host and a port\
		\nexample: %(prog)s -H 192.168.1.1 -p  80 [--arg="-Pn -sUV"]
	''')
	parser.add_argument('-H', dest = 'host', help = 'specify a hostname')
	parser.add_argument('-p', dest = 'port',  help = 'specify a port number, [cg:common port,others you should specify]')
	parser.add_argument('--arg', dest = 'arguments', nargs='?', type = str, help = 'specify a argument[default:-sV]')#nargs设置可选的参数
	args = parser.parse_args()
	if not args.host or not args.port:
		parser.print_help()
		sys.exit(1)
	print('args is ',args)
	Host = args.host
	if args.port == 'cg':
		Port = cg_ports
	else:
		Port = args.port
	if args.arguments is None:
		arg = '-sV'
		print('使用默认参数：-sV')#None 表示没有加参数
	else:
		arg =  args.arguments
		print('使用参数：{}'.format(args.arguments))#None 表示没有加参数
	#print(type(Port))#<class 'int'>,扫描参数应为字符
	Port = str(Port)
	nm = nmap.PortScanner()
	try:
		nm.scan(hosts = Host, ports = Port, arguments = arg)
		#print(arg)
		#print(nm[Host].hostname()) #'127.0.0.1-10'
		all_hosts = nm.all_hosts()
		print('需要扫描的主机列表：{}'.format(all_hosts))#主机ip 的list类型['xx', 'yy', 'zz', ...]
		for host in nm.all_hosts():

			print('========================================')
			print('Host : {0} ({1})'.format(host, nm[host].hostname()))
			print('host state : {0}'.format(nm[host].state()))
			#print(nm[host].all_protocols())
			for proto in nm[host].all_protocols():
				print('---------------')
				print('Protocol : {0}'.format(proto))
				lport = list(nm[host][proto].keys())	
				#print('lport : {}'.format(lport))
				lport.sort()
				for aport in lport:
					print('port : {0}\tstate : {1} {2} {3} {4}'.format(aport, \
					nm[host][proto][aport]['state'],   \
					nm[host][proto][aport]['product'], \
					nm[host][proto][aport]['version'], \
					nm[host][proto][aport]['extrainfo']))

		print('================It\'s over!==============\n')
	except Exception as e:
		print(e)


if __name__ == '__main__':
	main()

############################<<<<<<<<<<<<<上面就是nmap库导入扫描#########################
		
