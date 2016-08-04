# vi:set sw=4 ts=4 expandtab:
# -*- coding: utf8 -*-

import sys
import platform
import json
sys.path.insert(0, "../../")

from sdk.coolsms import Coolsms
from sdk.exceptions import CoolsmsException
from sdk.exceptions import CoolsmsSDKException
from sdk.exceptions import CoolsmsSystemException
from sdk.exceptions import CoolsmsServerException

## @class GroupMessage
#  @brief management group message, using Rest API
class GroupMessage:
    # Coolsms Object
    cool = None

    ## @brief initialize
    #  @param string api_key [required]
    #  @param string api_secret [required]
    def __init__(self, api_key, api_secret):
        self.cool = Coolsms(api_key, api_secret)

    ## @brief create create group ( HTTP Method GET )
    #  @param dictionary params {
    #  @param string charset [optional]
    #  @param string srk [optional]
    #  @param string mode [optional]
    #  @param string delay [optional]
    #  @param boolean force_sms [optional]
    #  @param string os_platform [optional]
    #  @param string dev_lang [optional]
    #  @param string sdk_version [optional]
    #  @param string app_version [optional] }
    #  @return JSONObject
    def create_group(self):
        response = self.cool.request_get('new_group')

        return response

    ## @brief get group list ( HTTP Method GET )
    #  @param None
    #  @return JSONArray
    def get_group_list(self):
        response = self.cool.request_get('group_list')

        return response

    ## @brief delete groups ( HTTP Method POST )
    #  @param string group_ids [required]
    #  @return JSONobject
    def delete_groups(self, group_ids):
        if group_ids == None:
            raise CoolsmsSDKException("parameter 'group_ids' is required", 201)

        params = {'group_ids':group_ids}
        response = self.cool.request_post('delete_groups', params)

        return response

    ## @brief get group info ( HTTP Method GET )
    #  @param string group_id [required]
    #  @return JSONObject
    def get_group_info(self, group_id):
        if group_id == None:
            raise CoolsmsSDKException("parameter 'group_id' is required", 201)

        resource = "groups/%s" % group_id
        response = self.cool.request_get(resource)

        return response

    ## @brief add message to group ( HTTP Method POST )
    #  @param dictionary params {
    #  @param string group_id [required]
    #  @param string to [required]
    #  @param string from [required]
    #  @param string text [required]
    #  @param string image_id [optional]
    #  @param string refname [optional]
    #  @param string country [optional]
    #  @param string datetime [optional]
    #  @param string subject [optional]
    #  @param integer delay [optional] }
    #  @return JSONObject
    def add_messages(self, params):
        # params type check
        if type(params) is not dict:
            raise CoolsmsSDKException("parameter type is not dictionary", 201)

        # require fields check
        if "group_id" not in params:
            raise CoolsmsSDKException("parameter 'group_id' is required", 201)

        params = Coolsms.check_send_data(params)

        # system info
        params['os_platform'] = platform.system()
        params['dev_lang'] = "Python %s" % platform.python_version()
        params['sdk_version'] = "sms-python %s" % Coolsms.sdk_version

        # request post
        resource = "groups/%s/add_messages" % params['group_id']
        response = self.cool.request_post(resource, params)

        return response

    ## @brief add json type message to group ( HTTP Method POST )
    #  @param string group_id [required]
    #  @param JSONArray messages [required] [{
    #  @param string to [required]
    #  @param string from [required]
    #  @param string text [required]
    #  @param string image_id [optional]
    #  @param string refname [optional]
    #  @param string country [optional]
    #  @param string datetime [optional]
    #  @param string subject [optional]
    #  @param integer delay [optional] }]
    #  @return JSONObject
    def add_messages_json(self, group_id, messages):
        # require fields check
        if group_id == None or messages == None:
            raise CoolsmsSDKException("parameter 'group_id', 'messages' are required", 201)
        
        messages = json.loads(messages)

        for data in messages:
            data = Coolsms.check_send_data(data)

        # messages setting
        params = dict()
        params['messages'] = json.dumps(messages)

        # system info
        params['os_platform'] = platform.system()
        params['dev_lang'] = "Python %s" % platform.python_version()
        params['sdk_version'] = "sms-python %s" % Coolsms.sdk_version

        # request post
        resource = "groups/%s/add_messages.json" % group_id
        response = self.cool.request_post(resource, params)

        return response

    ## @brief get message list ( HTTP Method GET )
    #  @param dictionary params {
    #  @param string group_id [required]
    #  @param integer offset [optional]
    #  @param integer limit [optional] }
    #  @return JSONObject
    def get_message_list(self, params):
        # require fields check
        if "group_id" not in params:
            raise CoolsmsSDKException("parameter 'group_id' is required", 201)

        # request post
        resource = "groups/%s/message_list" % params['group_id']
        response = self.cool.request_get(resource, params)

        return response
    
    ## @brief delete message from group ( HTTP Method POST )
    #  @param string group_id [required]
    #  @param string message_ids [required]
    #  @return JSONObject
    def delete_messages(self, group_id, message_ids):
        # require fields check
        if group_id == None or message_ids == None:
            raise CoolsmsSDKException("parameter 'group_id', 'message_ids' are required", 201)

        params = dict()
        params['message_ids'] = message_ids

        # request post
        resource = "groups/%s/delete_messages" % group_id
        response = self.cool.request_post(resource, params)

        return response

    ## @brief send group message ( HTTP Method POST )
    #  @param string group_id [required]
    #  @return JSONObject
    def send(self, group_id):
        # require filed check
        if group_id == None:
            raise CoolsmsSDKException("parameter 'group_id' is required", 201)

        # request post
        resource = "groups/%s/send" % group_id
        response = self.cool.request_post(resource)

        return response