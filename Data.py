board = {('a', 1): [('a', 2), ('b', 2), ('b', 1)],
         ('a', 2): [('a', 1), ('b', 2), ('a', 3)],
         ('a', 3): [('a', 2), ('b', 3), ('b', 4), ('a', 4)],
         ('a', 4): [('a', 3), ('b', 4), ('a', 5)],
         ('a', 5): [('a', 4), ('b', 5), ('b', 6), ('a', 6)],
         ('a', 6): [('a', 5), ('b', 6), ('a', 7)],
         ('a', 7): [('a', 6), ('b', 7), ('b', 8)],

         ('b', 1): [('a', 1), ('b', 2), ('c', 1)],
         ('b', 2): [('b', 1), ('a', 1), ('a', 2), ('c', 2), ('b', 3)],
         ('b', 3): [('b', 2), ('a', 3), ('c', 2), ('b', 4), ('c', 3)],
         ('b', 4): [('a', 3), ('a', 4), ('b', 3), ('c', 4), ('b', 5)],
         ('b', 5): [('b', 4), ('a', 5), ('c', 4), ('c', 5), ('b', 6)],
         ('b', 6): [('a', 6), ('a', 5), ('b', 5), ('b', 7), ('c', 6)],
         ('b', 7): [('a', 7), ('b', 6), ('b', 8), ('c', 7), ('c', 6)],
         ('b', 8): [('a', 7), ('b', 7), ('c', 8)],

         ('c', 1): [('b', 1), ('d', 1), ('d', 2), ('c', 2)],
         ('c', 2): [('c', 1), ('b', 2), ('d', 2), ('c', 3), ('b', 3)],
         ('c', 3): [('c', 2), ('b', 3), ('d', 3), ('c', 4), ('d', 4)],
         ('c', 4): [('c', 3), ('b', 4), ('d', 4), ('c', 5), ('b', 5)],
         ('c', 5): [('c', 4), ('c', 6), ('b', 5), ('d', 5), ('d', 6)],
         ('c', 6): [('c', 5), ('c', 7), ('b', 6), ('d', 6), ('b', 7)],
         ('c', 7): [('c', 8), ('c', 6), ('b', 7), ('d', 7), ('d', 8)],
         ('c', 8): [('b', 8), ('d', 8), ('c', 7)],

         ('d', 1): [('c', 1), ('e', 1), ('d', 2)],
         ('d', 2): [('d', 1), ('c', 1), ('c', 2), ('e', 2), ('d', 3)],
         ('d', 3): [('d', 2), ('d', 4), ('e', 3), ('c', 3), ('e', 2)],
         ('d', 4): [('c', 4), ('e', 4), ('d', 3), ('d', 5), ('c', 3)],
         ('d', 5): [('c', 5), ('e', 5), ('d', 4), ('d', 6), ('e', 4)],
         ('d', 6): [('d', 5), ('d', 7), ('e', 6), ('c', 6), ('c', 5)],
         ('d', 7): [('d', 8), ('d', 6), ('e', 7), ('c', 7), ('e', 6)],
         ('d', 8): [('e', 8), ('c', 8), ('d', 7), ('c', 7)],

         ('e', 1): [('d', 1), ('f', 1), ('f', 2), ('e', 2)],
         ('e', 2): [('e', 1), ('f', 2), ('d', 2), ('e', 3), ('d', 3)],
         ('e', 3): [('e', 2), ('f', 3), ('d', 3), ('e', 4), ('f', 4)],
         ('e', 4): [('e', 3), ('e', 5), ('f', 4), ('d', 4), ('d', 5)],
         ('e', 5): [('e', 4), ('e', 6), ('f', 5), ('d', 5), ('f', 6)],
         ('e', 6): [('e', 5), ('e', 7), ('f', 6), ('d', 6), ('d', 7)],
         ('e', 7): [('e', 6), ('e', 8), ('f', 7), ('d', 7), ('f', 8)],
         ('e', 8): [('f', 8), ('d', 8), ('e', 7)],

         ('f', 1): [('f', 2), ('e', 1), ('g', 1)],
         ('f', 2): [('f', 1), ('e', 1), ('f', 3), ('g', 2), ('e', 2)],
         ('f', 3): [('f', 2), ('f', 4), ('g', 3), ('e', 3), ('g', 2)],
         ('f', 4): [('f', 3), ('f', 5), ('g', 4), ('e', 4), ('e', 3)],
         ('f', 5): [('f', 4), ('f', 6), ('g', 5), ('e', 5), ('g', 4)],
         ('f', 6): [('f', 5), ('f', 7), ('g', 6), ('e', 6), ('e', 5)],
         ('f', 7): [('f', 8), ('f', 6), ('g', 7), ('e', 7), ('g', 6)],
         ('f', 8): [('f', 7), ('g', 8), ('e', 8), ('e', 7)],

         ('g', 1): [('h', 2), ('g', 2), ('f', 1)],
         ('g', 2): [('h', 2), ('f', 2), ('g', 1), ('g', 3), ('f', 3)],
         ('g', 3): [('g', 2), ('g', 4), ('h', 3), ('f', 3), ('h', 4)],
         ('g', 4): [('g', 3), ('g', 5), ('f', 4), ('h', 4), ('f', 5)],
         ('g', 5): [('g', 4), ('g', 6), ('h', 5), ('f', 5), ('h', 6)],
         ('g', 6): [('g', 5), ('g', 7), ('h', 6), ('f', 6), ('f', 7)],
         ('g', 7): [('g', 6), ('g', 8), ('h', 7), ('f', 7), ('h', 8)],
         ('g', 8): [('h', 8), ('g', 7), ('f', 8)],

         ('h', 2): [('g', 1), ('g', 2), ('h', 3)],
         ('h', 3): [('h', 2), ('g', 3), ('h', 4)],
         ('h', 4): [('h', 3), ('g', 3), ('g', 4), ('h', 5)],
         ('h', 5): [('h', 4), ('g', 5), ('h', 6)],
         ('h', 6): [('h', 5), ('g', 5), ('g', 6), ('h', 7)],
         ('h', 7): [('h', 6), ('g', 7), ('h', 8)],
         ('h', 8): [('g', 7), ('h', 7), ('g', 8)]
         }


positions = [
(('a', 1), (485, 173)),
(('a', 2), (578, 215)),
(('a', 3), (628, 298)),
(('a', 4), (715, 343)),
(('a', 5), (770, 422)),
(('a', 6), (862, 466)),
(('a', 7), (911, 541)),
(('b', 1), (393, 216)),
(('b', 2), (485, 260)),
(('b', 3), (532, 341)),
(('b', 4), (625, 384)),
(('b', 5), (678, 466)),
(('b', 6), (769, 508)),
(('b', 7), (819, 585)),
(('b', 8), (908, 628)),
(('c', 1), (339, 296)),
(('c', 2), (427, 340)),
(('c', 3), (482, 418)),
(('c', 4), (573, 466)),
(('c', 5), (624, 539)),
(('c', 6), (715, 587)),
(('c', 7), (765, 662)),
(('c', 8), (852, 705)),
(('d', 1), (246, 336)),
(('d', 2), (338, 383)),
(('d', 3), (391, 464)),
(('d', 4), (481, 504)),
(('d', 5), (534, 582)),
(('d', 6), (623, 626)),
(('d', 7), (672, 699)),
(('d', 8), (763, 745)),
(('e', 1), (192, 416)),
(('e', 2), (282, 460)),
(('e', 3), (337, 538)),
(('e', 4), (426, 581)),
(('e', 5), (478, 654)),
(('e', 6), (567, 704)),
(('e', 7), (619, 775)),
(('e', 8), (707, 819)),
(('f', 1), (99, 461)),
(('f', 2), (188, 504)),
(('f', 3), (245, 580)),
(('f', 4), (334, 623)),
(('f', 5), (388, 701)),
(('f', 6), (474, 743)),
(('f', 7), (528, 820)),
(('f', 8), (619, 860)),
(('g', 1), (46, 535)),
(('g', 2), (137, 580)),
(('g', 3), (193, 654)),
(('g', 4), (283, 699)),
(('g', 5), (334, 772)),
(('g', 6), (424, 817)),
(('g', 7), (475, 890)),
(('g', 8), (564, 933)),
(('h', 2), (53, 621)),
(('h', 3), (104, 699)),
(('h', 4), (193, 741)),
(('h', 5), (244, 817)),
(('h', 6), (334, 857)),
(('h', 7), (385, 933)),
(('h', 8), (474, 975))]

relativePositions = [
    (('a', 1), (3.9587628865979383, 6.242774566473988)),
    (('a', 2), (3.3217993079584773, 5.023255813953488)),
    (('a', 3), (3.0573248407643314, 3.6241610738255035)),
    (('a', 4), (2.6853146853146854, 3.1486880466472305)),
    (('a', 5), (2.4935064935064934, 2.559241706161137)),
    (('a', 6), (2.2273781902552203, 2.3175965665236054)),
    (('a', 7), (2.1075740944017562, 1.9963031423290203)),
    (('b', 1), (4.885496183206107, 5.0)),
    (('b', 2), (3.9587628865979383, 4.153846153846154)),
    (('b', 3), (3.6090225563909772, 3.167155425219941)),
    (('b', 4), (3.072, 2.8125)),
    (('b', 5), (2.831858407079646, 2.3175965665236054)),
    (('b', 6), (2.4967490247074124, 2.125984251968504)),
    (('b', 7), (2.3443223443223444, 1.8461538461538463)),
    (('b', 8), (2.1145374449339207, 1.7197452229299364)),
    (('c', 1), (5.663716814159292, 3.6486486486486487)),
    (('c', 2), (4.496487119437939, 3.176470588235294)),
    (('c', 3), (3.983402489626556, 2.583732057416268)),
    (('c', 4), (3.350785340314136, 2.3175965665236054)),
    (('c', 5), (3.076923076923077, 2.0037105751391464)),
    (('c', 6), (2.6853146853146854, 1.839863713798978)),
    (('c', 7), (2.5098039215686274, 1.6314199395770392)),
    (('c', 8), (2.2535211267605635, 1.5319148936170213)),
    (('d', 1), (7.804878048780488, 3.2142857142857144)),
    (('d', 2), (5.680473372781065, 2.8198433420365534)),
    (('d', 3), (4.910485933503836, 2.3275862068965516)),
    (('d', 4), (3.991683991683992, 2.142857142857143)),
    (('d', 5), (3.595505617977528, 1.8556701030927836)),
    (('d', 6), (3.081861958266453, 1.7252396166134185)),
    (('d', 7), (2.857142857142857, 1.5450643776824033)),
    (('d', 8), (2.5163826998689385, 1.4496644295302012)),
    (('e', 1), (10.0, 2.5961538461538463)),
    (('e', 2), (6.808510638297872, 2.347826086956522)),
    (('e', 3), (5.6973293768546, 2.007434944237918)),
    (('e', 4), (4.507042253521127, 1.8588640275387263)),
    (('e', 5), (4.01673640167364, 1.651376146788991)),
    (('e', 6), (3.386243386243386, 1.5340909090909092)),
    (('e', 7), (3.101777059773829, 1.3935483870967742)),
    (('e', 8), (2.7157001414427158, 1.3186813186813187)),
    (('f', 1), (19.393939393939394, 2.3427331887201737)),
    (('f', 2), (10.212765957446809, 2.142857142857143)),
    (('f', 3), (7.836734693877551, 1.8620689655172413)),
    (('f', 4), (5.748502994011976, 1.7335473515248796)),
    (('f', 5), (4.948453608247423, 1.5406562054208275)),
    (('f', 6), (4.050632911392405, 1.4535666218034993)),
    (('f', 7), (3.6363636363636362, 1.3170731707317074)),
    (('f', 8), (3.101777059773829, 1.255813953488372)),
    (('g', 1), (41.73913043478261, 2.0186915887850465)),
    (('g', 2), (14.014598540145986, 1.8620689655172413)),
    (('g', 3), (9.94818652849741, 1.651376146788991)),
    (('g', 4), (6.784452296819788, 1.5450643776824033)),
    (('g', 5), (5.748502994011976, 1.3989637305699483)),
    (('g', 6), (4.528301886792453, 1.3219094247246022)),
    (('g', 7), (4.042105263157895, 1.2134831460674158)),
    (('g', 8), (3.404255319148936, 1.157556270096463)),
    (('h', 2), (36.22641509433962, 1.7391304347826086)),
    (('h', 3), (18.46153846153846, 1.5450643776824033)),
    (('h', 4), (9.94818652849741, 1.45748987854251)),
    (('h', 5), (7.868852459016393, 1.3219094247246022)),
    (('h', 6), (5.748502994011976, 1.2602100350058343)),
    (('h', 7), (4.987012987012987, 1.157556270096463)),
    (('h', 8), (4.050632911392405, 1.1076923076923078))
]


UpperLeftOfSquars = [
    ('h',2),
    ('h',4),
    ('h',6),
    ('g',1),
    ('g',3),
    ('g',5),
    ('g',7),
    ('f',2),
    ('f',4),
    ('f',6),
    ('e',1),
    ('e',3),
    ('e',5),
    ('e',7),
    ('d',2),
    ('d',4),
    ('d',6),
    ('c',1),
    ('c',3),
    ('c',5),
    ('c',7),
    ('b',2),
    ('b',4),
    ('b',6)
]


'''
f = open('www.txt', 'a')
for i in positions:
    tu = (i[0],((1920.0/i[1][0]), (1080.0/i[1][1])))
    f.write(str(tu) + "\n")
'''