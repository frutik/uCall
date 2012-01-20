from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from config.models import Config
from channel_message import ChannelMessage

def _config_section(request, section_key):
    config = Config.objects.filter(section=section_key)
    #TODO is it possible to gzip/cache???
    return render_to_response('config/config.json', {'section': section_key, 'config': config}, mimetype = 'text/javascript')

@login_required()
def config_stomp(request):
    return _config_section(request, 'stomp')

@login_required()
def config_app(request):
    return _config_section(request, 'app')

@login_required()
def config_voip(request):
    return _config_section(request, 'voip')

@login_required()
def config_current_user(request):
    #TODO is it possible to gzip/cache???
    return render_to_response('config/current_user.json', {'user': request.user}, mimetype = 'text/javascript')

@login_required()
def config_channel_event_schema(request):
    #TODO is it possible to gzip/cache???
    message = ChannelMessage()
    return render_to_response('config/channel_event_schema.json', {'schema': message.dump_schema_json()}, mimetype = 'text/javascript')

@login_required()
def config_urls(request):
    #TODO is it possible to gzip/cache???
    return render_to_response('config/urls.json', {'user': request.user}, mimetype = 'text/javascript')

