from mock import Mock
from contextlib import contextmanager
from hamcrest import assert_that, instance_of, equal_to
from hamcrest.core.helpers.wrap_matcher import wrap_matcher, is_matchable_type
from matchmock import called, not_called, called_once, called_with


class RaisesContext(object):
    exception = None


@contextmanager
def assert_raises(matcher=None, message=''):
    # Short hand for instance_of matcher
    if is_matchable_type(matcher):
        matcher = instance_of(matcher)
    else:
        matcher = wrap_matcher(matcher)

    context = RaisesContext()
    try:
        yield context
    except Exception as e:
        context.exception = e

    assert_that(context.exception, matcher, message)


def test_called_ok():
    mock = Mock()
    mock()

    assert_that(mock, called())


def test_called_ok_twice():
    mock = Mock()
    mock()
    mock()

    assert_that(mock, called())


def test_called_fail():
    expected = '''
Expected: Mock called a value greater than <0> times with ANYTHING
     but: was called 0 times
'''

    mock = Mock()

    with assert_raises(AssertionError) as e:
        assert_that(mock, called())

    assert_that(str(e.exception), equal_to(expected))


def test_not_called_ok():
    mock = Mock()

    assert_that(mock, not_called())


def test_not_called_fail():
    expected = '''
Expected: Mock called <0> times with ANYTHING
     but: was called 1 times with (<('foo',)>, <{}>)
'''

    mock = Mock()
    mock('foo')

    with assert_raises(AssertionError) as e:
        assert_that(mock, not_called())

    assert_that(str(e.exception), equal_to(expected))


def test_called_once_ok():
    mock = Mock()
    mock('foo')

    assert_that(mock, called_once())


def test_called_once_fail_not_called():
    expected = '''
Expected: Mock called <1> times with ANYTHING
     but: was called 0 times
'''

    mock = Mock()

    with assert_raises(AssertionError) as e:
        assert_that(mock, called_once())

    assert_that(str(e.exception), equal_to(expected))


def test_called_once_fail_called_twice():
    expected = '''
Expected: Mock called <1> times with ANYTHING
     but: was called 2 times with (<('foo',)>, <{}>) and (<('bar',)>, <{}>)
'''

    mock = Mock()
    mock('foo')
    mock('bar')

    with assert_raises(AssertionError) as e:
        assert_that(mock, called_once())

    assert_that(str(e.exception), equal_to(expected))


def test_called_with_ok():
    mock = Mock()
    mock('foo', 5)

    assert_that(mock, called_with('foo', instance_of(int)))


def test_called_with_ok_kwargs():
    mock = Mock()
    mock(x='foo', y=5)

    assert_that(mock, called_with(x='foo', y=instance_of(int)))


def test_called_with_ok_multi():
    mock = Mock()
    mock('baz')
    mock('foo', 5)
    mock('bar', 5)

    assert_that(mock, called_with('foo', instance_of(int)))


def test_called_with_failed():
    expected = '''
Expected: Mock called a value greater than <0> times with \
('foo', an instance of int, )
     but: was called 1 times with (<('foo', 'bar')>, <{}>)
'''
    mock = Mock()
    mock('foo', 'bar')

    with assert_raises(AssertionError) as e:
        assert_that(mock, called_with('foo', instance_of(int)))

    assert_that(str(e.exception), equal_to(expected))


def test_called_with_kwarg_failed():
    expected = '''
Expected: Mock called a value greater than <0> times with ('foo', egg='spam')
     but: was called 1 times with (<('foo', 'bar')>, <{}>)
'''
    mock = Mock()
    mock('foo', 'bar')

    with assert_raises(AssertionError) as e:
        assert_that(mock, called_with('foo', egg='spam'))

    assert_that(str(e.exception), equal_to(expected))


def test_called_with_extra_kwarg():
    expected = '''
Expected: Mock called a value greater than <0> times with ('spam', )
     but: was called 1 times with (<('spam',)>, <{'foo': 'bar'}>)
'''
    mock = Mock()
    mock('spam', foo='bar')

    with assert_raises(AssertionError) as e:
        assert_that(mock, called_with('spam'))

    assert_that(str(e.exception), equal_to(expected))
