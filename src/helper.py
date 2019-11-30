def parse_req_body(body):
    body = body.decode('utf-8')
    pair_list = body.split('&')
    parsed_body = {}
    for pair in pair_list:
        pair = pair.split('=')
        parsed_body[pair[0]] = pair[1].replace('+',' ')
    return parsed_body

def userTypeChecker(user): 
    return lambda userType: len(userType.objects.filter(user=user)) > 0