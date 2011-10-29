from django.http import HttpResponse
from django.template import Context,RequestContext
from django.template.loader import get_template
import random
from django.core.context_processors import csrf
from main.models import *
import json
import urllib2,urllib,urlparse
from django.shortcuts import render,redirect
app_id="220712371281200"
app_secret="96abf470be341a7d3d9b23ea96ec7ce4"
def home(request):
	if 'current_user' in request.session:
		temp=render(request,"loggedinhome.html",{'current_user':request.session['current_user']})
	else:
		temp=redirect("http://localhost:8080/facebook")
	return temp
def view(request):
	shits=shit.objects.all()
	var={'shits':shits,'current_user':request.session['current_user']}
	output=render(request,"view.html",var)
	return output
def callback(request):
	global app_id,app_secret
	auth_code=request.GET['code']
	data={'client_id':app_id,'redirect_uri':'http://localhost:8080/callback','client_secret':app_secret,'code':auth_code}
	data=urllib.urlencode(data)
	url="https://graph.facebook.com/oauth/access_token?"+data
	response=urllib2.urlopen(url).read()
	response_prsd=urlparse.parse_qs(response)
	access_token=response_prsd['access_token'][0]
	graph_url="https://graph.facebook.com/me?access_token="+access_token
	response=urllib2.urlopen(graph_url).read()
	json_decode=json.loads(response)
	uid=json_decode['id']
	name=json_decode['name']
	photo='http://graph.facebook.com/'+uid+'/picture?type=normal'
	try:
		current_user=user.objects.get(uid=uid)
	except:
		current_user=user(uid=uid,name=name,photo=photo,access_token=access_token)
		current_user.save()
	request.session['current_user']=current_user.uid
	
	return redirect("http://localhost:8080")

def FBAuth(request):
	global app_id
	url="https://www.facebook.com/dialog/oauth?client_id="+app_id+"&redirect_uri=http://localhost:8080/callback"
	var={'url':url}
	output=render(request,"facebook.html",var)
	return HttpResponse(output)
def logout(request):
	del request.session['current_user']
	return redirect("http://localhost:8080")

def post(request):
	if 'text' in request.POST:
		text=request.POST['text']
		uid=request.POST['id']
		u=user.objects.get(uid=uid)
		new_shit=shit(user=u,text=text)
		new_shit.save()
		response=render(request,"posted.html",{'current_user':request.session['current_user']})
	else:
		all_users=user.objects.all()
		rnd_user=random.choice(all_users)
		var={'user':rnd_user,'current_user':request.session['current_user']}
		response=render(request,"post.html",var)
	return response

