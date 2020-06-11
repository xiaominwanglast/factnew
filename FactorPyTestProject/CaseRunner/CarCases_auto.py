#coding:utf-8
from ProductApi.CarDecisionApiAuto import CarDecisionApiAuto
env='T1'
serial_no_list = []
# serial_no_list.append(CarDecisionApiAuto(env=env,productId='CDW',sceneId='approval').makeDecision(certId='321321199109012916',phone='18301924915',userName=u'王孝敏',registerLocation='027008',agentName='1126'))
# serial_no_list.append(CarDecisionApiAuto(env=env,productId='CDW',sceneId='approval').makeDecision(certId='410881198808170841',phone='13520845565',userName=u'陈园园',registerLocation='027008',agentName='1126'))
# serial_no_list.append(CarDecisionApiAuto(env=env,productId='CDW',sceneId='approval').makeDecision(certId='431126198706237015',phone='13028807803',userName=u'宇文拓',registerLocation='027008',agentName='1126'))
serial_no_list.append(CarDecisionApiAuto(env=env,productId='CDW',sceneId='approval').makeDecision(certId='321321199109012916',phone='18301924915',userName=u'王孝敏',test_data={}))
# serial_no_list.append(CarDecisionApiAuto(env=env,productId='CDW',sceneId='approval').makeDecision(certId='532425198002051030', phone='15808665909', userName=u'普云春'))
# serial_no_list.append(CarDecisionApiAuto(env=env,productId='CDW',sceneId='approval').makeDecision(certId='45092319880724617X',phone='18301924915',userName=u'庞伟东'))
# serial_no_list.append(CarDecisionApiAuto(env=env,productId='CDW',sceneId='approval').makeDecision(certId='132828197402152369',phone='15632645636',userName=u'刘二争'))
# serial_no_list.append(CarDecisionApiAuto(env=env,productId='CDW',sceneId='approval').makeDecision(certId='640211197510256032',phone='13995066188',userName=u'张新年'))
# serial_no_list.append(CarDecisionApiAuto(env=env,productId='CDW',sceneId='approval').makeDecision(certId='452527198007280471',phone='15977979068',userName=u'陈广德',agentName='1047'))
# print(CarDecisionApiAuto(env=env,productId='CDW',sceneId='approval').getDecisionResult(serial_no='1563849394061-096B7E3237DB754C5494B7B5AA3F1BD1'))
print (serial_no_list)
