from graphs import graph_matches

__author__ = 'ubuntu'

json = [
{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/portrait_large/11126024515_f7ba791926_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/10999518716_2fa45e59af_o.jpg/desc.lbp',
 'img_a': './portrait_large/11126024515_f7ba791926_o.jpg',
 'img_b': './portrait_large/10999518716_2fa45e59af_o.jpg',
 'weight': 0.4781784159761504},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11112681864_a3c9b88807_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/10999518716_2fa45e59af_o.jpg/desc.lbp',
 'img_a': './maps/11112681864_a3c9b88807_o.jpg',
 'img_b': './portrait_large/10999518716_2fa45e59af_o.jpg',
 'weight': 0.48754824823940013},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/portrait_large/11147081785_e078f18351_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/10999518716_2fa45e59af_o.jpg/desc.lbp',
 'img_a': './portrait_large/11147081785_e078f18351_o.jpg',
 'img_b': './portrait_large/10999518716_2fa45e59af_o.jpg',
 'weight': 0.5477396699825468},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11296802974_eee165c458_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/10999518716_2fa45e59af_o.jpg/desc.lbp',
 'img_a': './maps/11296802974_eee165c458_o.jpg',
 'img_b': './portrait_large/10999518716_2fa45e59af_o.jpg',
 'weight': 0.5502616838907454},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11296928893_ed503f8072_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/10999518716_2fa45e59af_o.jpg/desc.lbp',
 'img_a': './maps/11296928893_ed503f8072_o.jpg',
 'img_b': './portrait_large/10999518716_2fa45e59af_o.jpg',
 'weight': 0.5512399822598217},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/portrait_large/11040852736_52057d19e1_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/10999518716_2fa45e59af_o.jpg/desc.lbp',
 'img_a': './portrait_large/11040852736_52057d19e1_o.jpg',
 'img_b': './portrait_large/10999518716_2fa45e59af_o.jpg',
 'weight': 0.5625137026497349},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11296720486_4c968c5e64_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/10999518716_2fa45e59af_o.jpg/desc.lbp',
 'img_a': './maps/11296720486_4c968c5e64_o.jpg',
 'img_b': './portrait_large/10999518716_2fa45e59af_o.jpg',
 'weight': 0.5808820057956771},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11204289353_c2f0fb7727_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/10999518716_2fa45e59af_o.jpg/desc.lbp',
 'img_a': './maps/11204289353_c2f0fb7727_o.jpg',
 'img_b': './portrait_large/10999518716_2fa45e59af_o.jpg',
 'weight': 0.6064681585764697},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/portrait_large/11095352184_2cf93e0f02_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/10999518716_2fa45e59af_o.jpg/desc.lbp',
 'img_a': './portrait_large/11095352184_2cf93e0f02_o.jpg',
 'img_b': './portrait_large/10999518716_2fa45e59af_o.jpg',
 'weight': 0.6957597988617015},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/portrait_large/11126024515_f7ba791926_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/11095352184_2cf93e0f02_o.jpg/desc.lbp',
 'img_a': './portrait_large/11126024515_f7ba791926_o.jpg',
 'img_b': './portrait_large/11095352184_2cf93e0f02_o.jpg',
 'weight': 0.8570746520382365},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/portrait_large/11095352184_2cf93e0f02_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/maps/11112681864_a3c9b88807_o.jpg/desc.lbp',
 'img_a': './portrait_large/11095352184_2cf93e0f02_o.jpg',
 'img_b': './maps/11112681864_a3c9b88807_o.jpg',
 'weight': 0.8666202266606373},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11296928893_ed503f8072_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/11095352184_2cf93e0f02_o.jpg/desc.lbp',
 'img_a': './maps/11296928893_ed503f8072_o.jpg',
 'img_b': './portrait_large/11095352184_2cf93e0f02_o.jpg',
 'weight': 0.9040257580525395},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11296802974_eee165c458_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/11095352184_2cf93e0f02_o.jpg/desc.lbp',
 'img_a': './maps/11296802974_eee165c458_o.jpg',
 'img_b': './portrait_large/11095352184_2cf93e0f02_o.jpg',
 'weight': 0.9122129221671109},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/portrait_large/11147081785_e078f18351_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/11095352184_2cf93e0f02_o.jpg/desc.lbp',
 'img_a': './portrait_large/11147081785_e078f18351_o.jpg',
 'img_b': './portrait_large/11095352184_2cf93e0f02_o.jpg',
 'weight': 0.9137842238666902},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/portrait_large/11095352184_2cf93e0f02_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/11040852736_52057d19e1_o.jpg/desc.lbp',
 'img_a': './portrait_large/11095352184_2cf93e0f02_o.jpg',
 'img_b': './portrait_large/11040852736_52057d19e1_o.jpg',
 'weight': 0.9172260476613256},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11296720486_4c968c5e64_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/11095352184_2cf93e0f02_o.jpg/desc.lbp',
 'img_a': './maps/11296720486_4c968c5e64_o.jpg',
 'img_b': './portrait_large/11095352184_2cf93e0f02_o.jpg',
 'weight': 0.927180840866131},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11204289353_c2f0fb7727_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/11126024515_f7ba791926_o.jpg/desc.lbp',
 'img_a': './maps/11204289353_c2f0fb7727_o.jpg',
 'img_b': './portrait_large/11126024515_f7ba791926_o.jpg',
 'weight': 0.9586573751460813},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11204289353_c2f0fb7727_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/maps/11112681864_a3c9b88807_o.jpg/desc.lbp',
 'img_a': './maps/11204289353_c2f0fb7727_o.jpg',
 'img_b': './maps/11112681864_a3c9b88807_o.jpg',
 'weight': 0.9639979180671807},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11204289353_c2f0fb7727_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/11095352184_2cf93e0f02_o.jpg/desc.lbp',
 'img_a': './maps/11204289353_c2f0fb7727_o.jpg',
 'img_b': './portrait_large/11095352184_2cf93e0f02_o.jpg',
 'weight': 0.9642014906169772},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11296928893_ed503f8072_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/maps/11204289353_c2f0fb7727_o.jpg/desc.lbp',
 'img_a': './maps/11296928893_ed503f8072_o.jpg',
 'img_b': './maps/11204289353_c2f0fb7727_o.jpg',
 'weight': 0.9814151840500368},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11296720486_4c968c5e64_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/11126024515_f7ba791926_o.jpg/desc.lbp',
 'img_a': './maps/11296720486_4c968c5e64_o.jpg',
 'img_b': './portrait_large/11126024515_f7ba791926_o.jpg',
 'weight': 0.9846092621393276},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11296802974_eee165c458_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/maps/11204289353_c2f0fb7727_o.jpg/desc.lbp',
 'img_a': './maps/11296802974_eee165c458_o.jpg',
 'img_b': './maps/11204289353_c2f0fb7727_o.jpg',
 'weight': 0.984975892906664},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11204289353_c2f0fb7727_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/11147081785_e078f18351_o.jpg/desc.lbp',
 'img_a': './maps/11204289353_c2f0fb7727_o.jpg',
 'img_b': './portrait_large/11147081785_e078f18351_o.jpg',
 'weight': 0.9852808745429068},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11204289353_c2f0fb7727_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/11040852736_52057d19e1_o.jpg/desc.lbp',
 'img_a': './maps/11204289353_c2f0fb7727_o.jpg',
 'img_b': './portrait_large/11040852736_52057d19e1_o.jpg',
 'weight': 0.9861391397523382},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11296720486_4c968c5e64_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/maps/11112681864_a3c9b88807_o.jpg/desc.lbp',
 'img_a': './maps/11296720486_4c968c5e64_o.jpg',
 'img_b': './maps/11112681864_a3c9b88807_o.jpg',
 'weight': 0.987572369235433},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/portrait_large/11126024515_f7ba791926_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/11040852736_52057d19e1_o.jpg/desc.lbp',
 'img_a': './portrait_large/11126024515_f7ba791926_o.jpg',
 'img_b': './portrait_large/11040852736_52057d19e1_o.jpg',
 'weight': 0.9904892358414747},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11296802974_eee165c458_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/11126024515_f7ba791926_o.jpg/desc.lbp',
 'img_a': './maps/11296802974_eee165c458_o.jpg',
 'img_b': './portrait_large/11126024515_f7ba791926_o.jpg',
 'weight': 0.9909207200768064},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/portrait_large/11147081785_e078f18351_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/11126024515_f7ba791926_o.jpg/desc.lbp',
 'img_a': './portrait_large/11147081785_e078f18351_o.jpg',
 'img_b': './portrait_large/11126024515_f7ba791926_o.jpg',
 'weight': 0.9911712372855486},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11296720486_4c968c5e64_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/maps/11204289353_c2f0fb7727_o.jpg/desc.lbp',
 'img_a': './maps/11296720486_4c968c5e64_o.jpg',
 'img_b': './maps/11204289353_c2f0fb7727_o.jpg',
 'weight': 0.9916333790594484},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11112681864_a3c9b88807_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/11040852736_52057d19e1_o.jpg/desc.lbp',
 'img_a': './maps/11112681864_a3c9b88807_o.jpg',
 'img_b': './portrait_large/11040852736_52057d19e1_o.jpg',
 'weight': 0.9927919962765214},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/portrait_large/11147081785_e078f18351_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/maps/11112681864_a3c9b88807_o.jpg/desc.lbp',
 'img_a': './portrait_large/11147081785_e078f18351_o.jpg',
 'img_b': './maps/11112681864_a3c9b88807_o.jpg',
 'weight': 0.9932720429857136},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11296928893_ed503f8072_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/11126024515_f7ba791926_o.jpg/desc.lbp',
 'img_a': './maps/11296928893_ed503f8072_o.jpg',
 'img_b': './portrait_large/11126024515_f7ba791926_o.jpg',
 'weight': 0.9937294382410856},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11296802974_eee165c458_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/maps/11112681864_a3c9b88807_o.jpg/desc.lbp',
 'img_a': './maps/11296802974_eee165c458_o.jpg',
 'img_b': './maps/11112681864_a3c9b88807_o.jpg',
 'weight': 0.9939513412395442},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11296928893_ed503f8072_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/maps/11112681864_a3c9b88807_o.jpg/desc.lbp',
 'img_a': './maps/11296928893_ed503f8072_o.jpg',
 'img_b': './maps/11112681864_a3c9b88807_o.jpg',
 'weight': 0.995597340653466},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11296928893_ed503f8072_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/maps/11296720486_4c968c5e64_o.jpg/desc.lbp',
 'img_a': './maps/11296928893_ed503f8072_o.jpg',
 'img_b': './maps/11296720486_4c968c5e64_o.jpg',
 'weight': 0.9966179134007066},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11296802974_eee165c458_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/maps/11296720486_4c968c5e64_o.jpg/desc.lbp',
 'img_a': './maps/11296802974_eee165c458_o.jpg',
 'img_b': './maps/11296720486_4c968c5e64_o.jpg',
 'weight': 0.9974768655781717},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11296720486_4c968c5e64_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/11040852736_52057d19e1_o.jpg/desc.lbp',
 'img_a': './maps/11296720486_4c968c5e64_o.jpg',
 'img_b': './portrait_large/11040852736_52057d19e1_o.jpg',
 'weight': 0.9975392314324579},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11296720486_4c968c5e64_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/11147081785_e078f18351_o.jpg/desc.lbp',
 'img_a': './maps/11296720486_4c968c5e64_o.jpg',
 'img_b': './portrait_large/11147081785_e078f18351_o.jpg',
 'weight': 0.9977484019527717},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11296928893_ed503f8072_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/11147081785_e078f18351_o.jpg/desc.lbp',
 'img_a': './maps/11296928893_ed503f8072_o.jpg',
 'img_b': './portrait_large/11147081785_e078f18351_o.jpg',
 'weight': 0.9979023832011633},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/portrait_large/11147081785_e078f18351_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/11040852736_52057d19e1_o.jpg/desc.lbp',
 'img_a': './portrait_large/11147081785_e078f18351_o.jpg',
 'img_b': './portrait_large/11040852736_52057d19e1_o.jpg',
 'weight': 0.9982653231433761},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11296802974_eee165c458_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/11147081785_e078f18351_o.jpg/desc.lbp',
 'img_a': './maps/11296802974_eee165c458_o.jpg',
 'img_b': './portrait_large/11147081785_e078f18351_o.jpg',
 'weight': 0.9988280678428245},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11296802974_eee165c458_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/11040852736_52057d19e1_o.jpg/desc.lbp',
 'img_a': './maps/11296802974_eee165c458_o.jpg',
 'img_b': './portrait_large/11040852736_52057d19e1_o.jpg',
 'weight': 0.9988381574578576},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11296802974_eee165c458_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/maps/11296928893_ed503f8072_o.jpg/desc.lbp',
 'img_a': './maps/11296802974_eee165c458_o.jpg',
 'img_b': './maps/11296928893_ed503f8072_o.jpg',
 'weight': 0.9989780553752379},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/maps/11296928893_ed503f8072_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/portrait_large/11040852736_52057d19e1_o.jpg/desc.lbp',
 'img_a': './maps/11296928893_ed503f8072_o.jpg',
 'img_b': './portrait_large/11040852736_52057d19e1_o.jpg',
 'weight': 0.9992036104312595},


{'descriptor': '.lbp',
 'descriptor_1': '/scratch/lost-visions/descriptors/portrait_large/11126024515_f7ba791926_o.jpg/desc.lbp',
 'descriptor_2': '/scratch/lost-visions/descriptors/maps/11112681864_a3c9b88807_o.jpg/desc.lbp',
 'img_a': './portrait_large/11126024515_f7ba791926_o.jpg',
 'img_b': './maps/11112681864_a3c9b88807_o.jpg',
 'weight': 0.9992589192968643},
 ]

graph_matches(json)