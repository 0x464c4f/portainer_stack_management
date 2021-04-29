import portainer_api
from portainer_api.api.auth_api import AuthApi
from portainer_api.models.stack_list_response import StackListResponse
import yaml
import base64
import json
import sys
import os
from portainer_api.rest import ApiException   


class Portainer_Management:
    def __init__(self, username:str, password:str) -> None:
        self.configuration = portainer_api.Configuration()
        self.configuration.host = os.environ("PORTAINER_URL")
        self.configuration.verify_ssl = True
        self.username = username
        self.password = password
        self.client = portainer_api.ApiClient(self.configuration)
        authapi = portainer_api.AuthApi(self.client)
        self.access_token = self.authenticate(authapi, username, password)
        

    def authenticate(self, authapi:AuthApi, username, password):
        try:
            auth_body = portainer_api.AuthenticateUserRequest(username=self.username,password=self.password)
            api_response = authapi.authenticate_user(auth_body)
            access_token = api_response.jwt
            self.client.set_default_header(header_name="Authorization", header_value=access_token)
            print("Successfully authenticated")
        except ApiException as e:
            access_token = ""
            print("Exception when calling api: %s\n" % e)
        return access_token
    def does_secret_already_exist(self,secret_name,header):
        secret_exists = False
        try:
            response = self.client.request(method="GET",url=self.configuration.host+"/endpoints/1/docker/secrets",headers=header)
            data = json.loads(response.data)
            for secret in data:
                if secret["Spec"]["Name"]==secret_name:
                    secret_exists = secret["ID"]    
        except ApiException as e:
            print(f"Something wrong in the stack already exists call:{e}")
        return secret_exists
 
    def does_stack_already_exist(self,stack_name):
        try:
            stack_api_client = portainer_api.StacksApi(self.client)
            all_stacks:StackListResponse = stack_api_client.stack_list()
            stack_exists = False
            for stack in all_stacks:
                if stack_name==stack["Name"]:
                    stack_exists = stack["Id"]
            return stack_exists
        except ApiException as e:
            print(f"Something wrong in the stack already exists call:{e}")
 
    def create_or_update_stack_from_compose_file(self, compose_filename, stack_name, swarm_id=os.environ("SWARM_ID"),endpoint_id=1):
        ### include path to compose file if not in the same folder
        try:
            stack_api_client = portainer_api.StacksApi(self.client)
            stack_api_client.stack_list()
            with open(compose_filename) as file:
                file_loaded = yaml.load(file, Loader=yaml.FullLoader)
                yaml_string = yaml.dump(file_loaded,indent=2, width=10)
                stack_id =self.does_stack_already_exist(stack_name=stack_name)
                if stack_id:
                    body_stack_update = portainer_api.StackUpdateRequest(stack_file_content=yaml_string)
                    response = stack_api_client.stack_update(id=stack_id,body=body_stack_update,endpoint_id=endpoint_id)
                    print(f"Stack {stack_name} updated successfully")
                    print(response)
                else:
                    body_test_stack=portainer_api.StackCreateRequest(name=stack_name,swarm_id=swarm_id,stack_file_content=yaml_string)
                    response = stack_api_client.stack_create(type=1,method="string",endpoint_id=endpoint_id,body=body_test_stack)
                    print(f"Stack {stack_name} created successfully")
                    print(response)
        except ApiException as e:
            print("Exception when calling api: %s\n" % e)

    def remove_docker_secret():
        return 0

    def create_or_update_docker_secret(self,secret_name:str,secret_value:str,labels={}):
        secret_value_encoded = base64.b64encode(secret_value.encode("ascii")).decode("ascii")
        body = {"Name":secret_name,"Data":secret_value_encoded,"Labels":labels}
        header = {"Authorization": self.access_token}
        secret_id = self.does_secret_already_exist(secret_name,header)
        # Remove secret if it already exists - this is necessary to update it
        if secret_id:
            print(f"Secret {secret_name} exists already - is getting updated")
            try:
                response = self.client.request(method="DELETE",url=self.configuration.host+"/endpoints/1/docker/secrets/"+str(secret_id),headers=header)
                if response.status == 204:
                    print(f"Secret {secret_name} successfully deleted")
            except ApiException as e:
                print("Exception when calling api: %s\n" % e)
        # Create secret
        try:
            response = self.client.request(method="POST",url=self.configuration.host+"/endpoints/1/docker/secrets/create",body=body,headers=header)
            if response.status == 200:
                print(f"Secret {secret_name} successfully created")
        except ApiException as e:
            print("Exception when calling api: %s\n" % e)
        
        

# if __name__ == "__main__":
    #  If called as module it will create / update the specified stack
   
    # Create or update secret:
    # api.create_or_update_docker_secret("super_secret","leeet")
    #  Create or update stack example:
    # api.create_or_update_stack_from_compose(compose_filename=compose_filename,stack_name=stack_name)

