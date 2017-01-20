'''IBEIS IA REST API image upload, image metadata extraction, and detection.'''
# Author : Jason Parham 

import requests
import time
import uuid
import json
import os
from functools import partial
from multiprocessing.pool import Pool


DOMAIN = 'http://pachy.cs.uic.edu:5001'

def upload(image_path, signature='api/upload/image'):
    url = '%s/%s/' % (DOMAIN, signature)
    file_dict = {
        'image': open(image_path, 'rb'),
    }
    response = requests.post(url, files=file_dict)
    response_dict = response.json()
    assert response_dict['status']['success']
    return response_dict['response']

# def upload(image_path, flickrURL,signature='api/upload/image'):
#     url = '%s/%s/' % (DOMAIN, signature)
#     imgFl = str(image_path + str(os.path.basename(flickrURL)))
#     print(imgFl)
#     file_dict = {
#         'image': open(imgFl, 'rb'),
#     }
#     # response = requests.post(url, files=file_dict)
#     response_dict = response.json()
#     assert response_dict['status']['success']
#     return response_dict['response']


def check_job_status(jobid_str):
    data_dict = {
        'jobid': jobid_str,
    }
    response = get('api/engine/job/status', data_dict)
    jobstatus = response['jobstatus']
    assert jobstatus != 'exception'
    return jobstatus == 'completed'


def check_annot_metadata(aid_list):
    data_dict = {
        'aid_list': aid_list,
    }
    # bbox = (xtl, ytl, width, height)
    # where xtl = "X coordinate top left" and ytl = "Y coordinate top left"
    args = (get('api/annot/bbox', data_dict), )
    print('      bboxes      = %r' % args)
    args = (get('api/annot/theta', data_dict, skip_json=True), )
    print('      thetas      = %r' % args)
    args = (get('api/annot/species', data_dict, skip_json=True), )
    print('      species     = %r' % args)
    args = (get('api/annot/detect/confidence', data_dict, skip_json=True), )
    print('      confidences = %r' % args)
    args = (get('api/annot/note', data_dict, skip_json=True), )
    print('      notes       = %r' % args)


def _request(function, signature, data_dict, skip_json=False):
    url = '%s/%s/' % (DOMAIN, signature)

    if not skip_json:
        for key in data_dict:
            data_dict[key] = json.dumps(data_dict[key])
    response = function(url, data=data_dict)

    try:
        assert response.ok
    except AssertionError:
        print('!!! FAILED REQUEST !!!')
        print('\t URL      = %r' % (url, ))
        print('\t METHOD   = %r' % (function, ))
        print('\t RESPONSE = %s' % (response.text, ))
    response_dict = response.json()
    assert response_dict['status']['success']
    return response_dict['response']


def get(*args, **kwargs):
    return _request(requests.get, *args, **kwargs)


def put(*args, **kwargs):
    return _request(requests.put, *args, **kwargs)


def post(*args, **kwargs):
    return _request(requests.post, *args, **kwargs)


def delete(*args, **kwargs):
    return _request(requests.delete, *args, **kwargs)


def run_id_pipeline(aid): # ID'ing task for each annotation
    # step 1: get annot_uuid
    data_dict = {
        'aid_list': [aid],
    }
    annot_uuid_list = get('api/annot/uuid', data_dict)

    # step 2: for the given annot UUID run the detection against all the available annots
    data_dict = {
        'query_annot_uuid_list' : json.dumps([annot_uuid_list[0]])
    }
    response = requests.request('POST', url, data=data_dict)

    try:
        assert response.json()['status']['success']
    except AssertionError:
        print("RUN_ID_PIPELINE failed for annotation_id %i" %aid)

    jobid_str = response.json()['response']

    error_time = 60
    start = 0
    while not check_job_status(jobid_str) and start < error_time:
        print("Waiting..")
        start += 0
        time.sleep(5)

    try:
        assert check_job_status(jobid_str)
    except AssertionError:
        print("RUN_ID_PIPELINE failed for annotation_id %i" %aid)

    # step 3: Job execution must have successfully completed at this point and now we extract the needed information
    data_dict = {
        'jobid' : jobid_str
    }

    result = get("api/engine/job/result", data_dict)['json_result']['inference_dict']['cluster_dict']

    
    with open(aid_uuid_map_flickr.json, "r") as aid_uuid_map_json:
        aid_uuid_map = json.load(aid_uuid_map_json)

    with open(uuid_aid_map_flickr.json, "r") as uuid_aid_map_json:
        uuid_aid_map = json.load(uuid_aid_map_json)

    # check if there is a previously assigned name, if no name is assigned just assign the new_name_"n"
    name = None
    for i in range(len(result['orig_name_list'])):
        if 'NEW_NAME' not in result['orig_name_list'][i]:
            # this i has been previously assigned a name
            name = result['orig_name_list'][i]

    if name == None:
        name = re.findall(r'NEWNAME_(\d+)', result['new_name_list'][0])


    # make the final assignment
    for annot_uuid_dict in result['annot_uuid_list']:
        aid = uuid_aid_map[annot_uuid_dict["__UUID__"]]

        data_dict = {
            "aid_list" : [aid],
            "name_list" : [name]
        }
        r = put("api/annot/name", data_dict)
    return result

def run_detection_task(gid):
    data_dict = {
        'gid_list': [gid],
    }
    image_uuid_list = get('api/image/uuid', data_dict)
    image_uuid_dict = image_uuid_list[0]
    image_uuid = uuid.UUID(image_uuid_dict['__UUID__'])
    print("image_uuid %i" %image_uuid)

    # Run detection on the image (blocking)
    #    NOTE: IBEIS IA caches information, once detection has been run on an
    #          image, it will cache it for future detection runs, which will be
    #          much faster
    # Running detection takes time, this call is a blocking call
    # For a non-blocking detection call, look at
    # /api/engine/detect/cnn/yolo/ [POST] using the API job engine.  For an
    # example, see below.
    data_dict = {
        'gid_list': [gid],
    }

    aids_list = get('api/detect/cnn/yolo', data_dict)
    aid_list = aids_list[0]
    print('\nAnnot aid_list    = %r' % (aid_list, ))
    check_annot_metadata(aid_list)

    # Delete the annotation for second detection run
    print('\nDeleting aid_list = %r' % (aid_list, ))
    data_dict = {
        'aid_list': aid_list,
    }
    delete('api/annot', data_dict)
    # Sanity check, should be all empty
    check_annot_metadata(aid_list)

    # Run detection on the image using the job engine (non-blocking)
    # This call is a post call that takes in image UUIDs.  The easiest way to
    # encode Python UUID objects is to simply JSON-ify them.
    data_dict = {
        'image_uuid_list': image_uuid_list,
    }
    jobid_str = post('api/engine/detect/cnn/yolo', data_dict)

    print('\nEngine Job ID     = %r' % (jobid_str, ))

    # We immediately get a job engine ID, we need to query about the status of
    # the job periodically to check it's status and look for it to register as
    # completed
    patience = 60 * 5
    while not check_job_status(jobid_str):
        print('\t Checking status...')
        if patience < 0:
            break
        time.sleep(1)
        patience -= 1

    # The detection job has completed and the result (detected aids) have been
    # given to the engine.  Go get the result, which should be cached from the
    # first blocking detection call.
    # The job engine does not return aids, but rather detection results before
    # they have been committed as annotations.  You need to commit yourself
    data_dict = {
        'jobid': jobid_str,
    }
    result_list = get('api/engine/job/result', data_dict)
    detections_list = result_list['json_result']['results_list']
    detection_list = detections_list[0]
    print('Engine Detections = %r' % (detection_list, ))

    # Delete the annotation (again) before creating the annotation using the
    # detection results
    data_dict = {
        'aid_list': aid_list,
    }
    delete('api/annot', data_dict)

    # Add annotations based on detection results
    gid_list = [gid] * len(detection_list)
    bbox_list = [
        (
            detection['xtl'],
            detection['ytl'],
            detection['width'],
            detection['height'],
        )
        for detection in detection_list
    ]
    theta_list = [detection['theta'] for detection in detection_list]
    species_list = [detection['class'] for detection in detection_list]
    confidence_list = [detection['confidence'] for detection in detection_list]
    data_dict = {
        'gid_list': gid_list,
        'bbox_list': bbox_list,
        'theta_list': theta_list,
        'species_list': species_list,
        'confidence_list': confidence_list,
    }
    aid_list = post('api/annot', data_dict)
    print('\nAnnot aid_list    = %r' % (aid_list, ))
    check_annot_metadata(aid_list)

    # Change the note for an annotation
    print('\nNotes on aid_list = %r' % (aid_list, ))
    data_dict = {
        'aid_list': aid_list,
        'notes_list': ['this is a test note'] * len(aid_list),
    }
    put('api/annot/note', data_dict)
    check_annot_metadata(aid_list)

    # args = (DOMAIN, gid, )
    # print('\nReview the detection here: %s/turk/detection/?gid=%d' % args)
    # # raw_input('continue? [enter]')

    # # , delete the annotation we have added three times
    # data_dict = {
    #     'aid_list': aid_list,
    # }
    # delete('api/annot', data_dict)
    # print('\nDeleted aid_list  = %r' % (aid_list, ))

def __main__():
    gidList = [i for i in range(88,101)]

    detect = partial(run_detection_task)

    with Pool(2) as p:
        p.map(detect, gidList)

if __name__ == "__main__":
    # __main__()

    with open("../data/beautyFeatures_FlickrExtracts_full.json", "r") as jsonObj:
        flckrImgs = json.load(jsonObj)
    print("Staring upload!")
    imgPath = '/Users/sreejithmenon/Dropbox/Social_Media_Wildlife_Census/Flickr_Scrape/'
    gidFlNmDict = {upload(imgPath+img+'.jpg') : img for img in list(flckrImgs.keys())}  

    with open("../data/flickr_imgs_gid_flnm_map.json","w") as jsonFl:
        json.dump(gidFlNmDict, jsonFl, indent=4)
    
    # data_dict = {
    #     'gid_list': [1],
    # }
    # image_uuid_list = get('api/image/uuid', data_dict)

    # data_dict = {
    #     'image_uuid_list': image_uuid_list,
    # }
    # jobid_str = post('api/engine/detect/cnn/yolo', data_dict)

    # print(jobid_str)
    # data_dict = {
    #     'gid_list': [1725],
    # }

    # delete('api/image',data_dict)
    # with open("../data/fileURLS.dat","r") as urlListFl:
    #     urlList = urlListFl.read().split("\n")
    # for url in urlList:
    #     print("Uploading image : %s " %str(os.path.basename(url)))
    #     upload("/Users/sreejithmenon/Dropbox/Social_Media_Wildlife_Census/Flickr_Scrape/",url)
