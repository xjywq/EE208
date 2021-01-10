from collections import Counter

# f: comment content
def cut_comment_seg(f):
    ... ## f->seg_list : [xx, xx, xx, xx]
    c = Counter()
    for x in seg_list:
        if len(x) > 1 and x != '\r\n':
            c[x] += 1
    return c.most_common()