import uuid
import json
import os
import urllib
import datetime
import pytz#http://stackoverflow.com/questions/2331592/datetime-datetime-utcnow-why-no-tzinfo
from . import file_manage
from urlparse import urlparse
from .models import UserAuthID, FileSys, ShortLink

def create_basic_json_response(error_code, msg, status):
	json_response = json.loads('{}')
	json_response['error_code'] = error_code
	json_response['msg'] = msg
	json_response['status'] = status
	return json_response

def upload_file(request):
	req_auth_id = request.GET.get('authid', '')
	req_username = UserAuthID.objects.filter(authID = req_auth_id)[0].userName
	req_file_path = request.GET.get('filepath', '')
	file_path = os.path.join(req_username, req_file_path)
	
	mgr = file_manage.fileManage()

	if(mgr.is_exists(file_path)):#file exist at directory
		response_data = create_basic_json_response(1202, 'file already exist at server dir', 'error')
	elif(FileSys.objects.filter(path = file_path)):#file exist at DB
		response_data = create_basic_json_response(1205, 'file already exist at DB', 'error')
	else:

		content_type_httpheader = request.META.get('CONTENT_TYPE')#get http header parameter from client
		content_type = content_type_httpheader.split(';')[0]
		'''the POST request may be sent from HTML form or JS/Python'''
		if(content_type != 'text/plain'):#post request from html form element
			blist = []
			print "dfgdfgdf"
			count_begin = 0
			count_end = 0
			#seperate request.body and get file data
			for b in request.body:
				if(request.body[count_end]==b'\n'[0] and count_end>0 and request.body[count_end-1]==b'\r'[0]):
					blist.append(request.body[count_begin:count_end-1])
					count_begin = count_end + 1
				count_end = count_end + 1
			post_data_split_len = len(blist)
			boundary_begin = blist[0]
			boundary_end = blist[post_data_split_len-1]
			file_data = b''
			count_begin = 0
			count_end = 0
			countb = 0
			countrn = 0
			for b in request.body:
				if(request.body[countb]==b'\n'[0] and countb>0 and request.body[countb-1]==b'\r'[0]):
					countrn = countrn+1
				if(countrn==4 and count_begin==0):
					count_begin = countb+1
				elif(countrn==post_data_split_len-1 and count_end==0):
					count_end = countb-1
				countb = countb + 1

			file_data = request.body[count_begin:count_end]#this is the seperated file data
			
			#print('file data len: {0}'.format(len(file_data)))
			#print('post_data_split_len:{0}'.format(post_data_split_len))
			#print('boundary_begin:{0}'.format(boundary_begin))
			#print('boundary_end:{0}'.format(boundary_end))
			#print('file_data:{0}'.format(file_data))
			stat = mgr.create_file(file_path, file_data)
			print stat[0]
			if(stat[0]):
				#create file correctly, then save the file info into DB
				print "here"
				parent_folder_path = os.path.dirname(file_path)
				parent_folder_id = FileSys.objects.filter(path=parent_folder_path)[0].id 
				
				file_guid = str(uuid.uuid1()).replace('-', 'x')
				file_parentid = parent_folder_id
				file_type = 'file'
				file_size = str(count_end-count_begin)
				file_current_date = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
				file_creator = req_username
				file_name = os.path.basename(file_path)
				file_item = FileSys(id=file_guid, parentid=file_parentid, type=file_type, size=file_size, createdate=file_current_date, creator=file_creator, filename=file_name, path=file_path)
				file_item.save()	
				
				response_data = create_basic_json_response(1200, 'file uploaded by form successfully', 'success')
			else:
				response_data = create_basic_json_response(1203, 'Exception:{0}'.format(stat[1]), 'error')
		else:#if the post request from pure post, the request.body is file content
			print "Love"
			stat = mgr.create_file(file_path, request.body)
			print stat[0]
			if(stat[0]):
				parent_folder_path = os.path.dirname(file_path)
				print parent_folder_path
				parent_folder_id = FileSys.objects.filter(path=parent_folder_path)[0].id 
				print parent_folder_id
				file_guid = str(uuid.uuid1()).replace('-', 'x')
				file_parentid = parent_folder_id
				file_type = 'file'
				file_size = str(len(request.body))
				file_current_date = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
				file_creator = req_username
				file_name = os.path.basename(file_path)
				file_item = FileSys(id=file_guid, parentid=file_parentid, type=file_type, size=file_size, createdate=file_current_date, creator=file_creator, filename=file_name, path=file_path)
				file_item.save()				
				print "210, 'file uploaded by POST successfully', 'success'"
				response_data = create_basic_json_response(1210, 'file uploaded by POST successfully', 'success')
			else:
				response_data = create_basic_json_response(1204, 'Exception:{0}'.format(stat[1]), 'success')
	return response_data

def download_file_link(request):
	req_auth_id = request.GET.get('authid', '')
	req_username = UserAuthID.objects.filter(authID = req_auth_id)[0].userName
	req_file_path = request.GET.get('filepath', '')
	file_path = os.path.join(req_username, req_file_path)
	
	mgr = file_manage.fileManage()
	if(mgr.is_exists(file_path) and FileSys.objects.filter(path = file_path)):#file exist at directory and DB
		short_id = str(uuid.uuid1())
		full_url_path = request.build_absolute_uri() 
		
		count_while = 0
		#repeat 5 times if uuid repeated
		while(ShortLink.objects.filter(id=short_id)):
			short_id = str(uuid.uuid1())
			count_while = count_while + 1
			if(count_while>=6):
				break
		if(ShortLink.objects.filter(id=short_id)):
			response_data = create_basic_json_response(1222, 'server busy, repeat again', 'error')
		else:#generate and send out short link for file downloading
			link_item = ShortLink(id=short_id, link=full_url_path)
			link_item.save()
			short_url = 'http://{0}/v1/f?id={1}'.format(request.META['HTTP_HOST'], short_id)
			response_data = create_basic_json_response(1220, short_url, 'success')
		
	else:
		response_data = create_basic_json_response(1221, 'file not exists', 'error')

	return response_data
	
def get_download_file_data(short_id):
	if(ShortLink.objects.filter(id=short_id)):
		url = ShortLink.objects.filter(id=short_id)[0].link
		print url
		url_p = urlparse(url)
		url_query = {}#split the url query "authid=7be9a910-5cde-11e5-b465-ea9f05b65156&op=download&filepath=testformpost.txt"
		for item in url_p.query.split('&'):
			url_query[item.split('=')[0]] = item.split('=')[1]
		#get file path
		req_username = UserAuthID.objects.filter(authID = url_query['authid'])[0].userName
		req_file_path = url_query['filepath']
		file_path = os.path.join(req_username, req_file_path)
		mgr = file_manage.fileManage()
		status, data = mgr.get_file_data(file_path)
		return os.path.basename(file_path), data#file name, file data
	else:
		print('the short link is invalid')
	pass
	
	
def api_file(request):
	'''authid should be validated before this function'''
	response_data = create_basic_json_response(1206, 'Incorrect API format, please check manual', 'error')
	req_op = request.GET.get('op', '')
	
	if(request.method == 'POST'):
		if(req_op == 'upload'):
			response_data = upload_file(request)
		else:
			response_data = create_basic_json_response(1201, 'not support this op', 'error')
	else:
		if(req_op == 'download'):
			response_data = download_file_link(request)
	
	return response_data