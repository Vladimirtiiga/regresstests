from getisightstatus import get_status
import os
token = os.getenv('tokendev')
get_status('18596' , token)