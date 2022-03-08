from __future__ import print_function
import timeit

domain = 'some_really_long_example.com'
lang = 'en'
path = 'some/really/long/path/'
iterations = 10000000


def meth_plus():
    '''Using + operator'''
    return 'http://' + domain + '/' + lang + '/' + path


def meth_join():
    '''Using ''.join()'''
    return ''.join(['http://', domain, '/', lang, '/', path])


def meth_form():
    '''Using string.format'''
    return 'http://{0}/{1}/{2}'.format(domain, lang, path)


def meth_intp():
    '''Using string interpolation'''
    return 'http://%s/%s/%s' % (domain, lang, path)


def meth_fstr():
    '''Using f-string interpolation'''
    return f'http://{domain}/{lang}/{path}'


plus = timeit.Timer(stmt="meth_plus()", setup="from __main__ import meth_plus")
join = timeit.Timer(stmt="meth_join()", setup="from __main__ import meth_join")
form = timeit.Timer(stmt="meth_form()", setup="from __main__ import meth_form")
intp = timeit.Timer(stmt="meth_intp()", setup="from __main__ import meth_intp")
fstr = timeit.Timer(stmt="meth_fstr()", setup="from __main__ import meth_fstr")

plus.val = plus.timeit(iterations)
join.val = join.timeit(iterations)
form.val = form.timeit(iterations)
intp.val = intp.timeit(iterations)
fstr.val = fstr.timeit(iterations)

min_val = min([plus.val, join.val, form.val, intp.val, fstr.val])

print('plus %0.12f (%0.2f%% as fast)' % (plus.val, (100 * min_val / plus.val), ))
print('join %0.12f (%0.2f%% as fast)' % (join.val, (100 * min_val / join.val), ))
print('form %0.12f (%0.2f%% as fast)' % (form.val, (100 * min_val / form.val), ))
print('intp %0.12f (%0.2f%% as fast)' % (intp.val, (100 * min_val / intp.val), ))
print('fstr %0.12f (%0.2f%% as fast)' % (fstr.val, (100 * min_val / fstr.val), ))