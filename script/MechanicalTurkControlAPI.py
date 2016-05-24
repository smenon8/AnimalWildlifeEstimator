# -*- coding: utf-8 -*-
"""
Created on Sat May 21 07:42:55 2016

@author: sreejithmenon
"""

import boto.mturk.connection as botoConn

conn = botoConn.MTurkConnection(aws_access_key_id='AKIAJFFU6MAGAWEDYXJA', aws_secret_access_key='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') 

listHIT = conn.get_reviewable_hits()

for hit in listHIT:
    assignments = conn.get_assignments(hit.HITId)
    for assign in assignments:
        if assign.AssignmentStatus == 'Submitted':
            conn.approve_assignment(assign.AssignmentId)
        else:
            print("Already approved, %s" %assign.AssignmentStatus)
    print("--------------------")

#
#        for ques_form_ans in assign.answers:
#			print(ques_form_ans.__dict__['markers'])
#
#
#
#
#for hit in hits:
#    assignments = mtc.get_assignments(hit.HITId)
#    for assignment in assignments:
#        print "Answers of the worker %s" % assignment.WorkerId
#        for question_form_answer in assignment.answers[0]:
#            for key, value in question_form_answer.fields:
#                print "%s: %s" % (key,value)
#        mtc.approve_assignment(assignment.AssignmentId)
#        print "--------------------"
#    mtc.disable_hit(hit.HITId)