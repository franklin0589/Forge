
import math


def Linear(t):
	""""Linear easing function."""
	return t

def EaseInSine(t):
	"""Ease in sine easing function."""
	return 1 - math.cos((t * math.pi) / 2)
def EaseOutSine(t):
	return math.sin((t * math.pi) / 2)
def EaseInOutSine(t):
    return -(math.cos(math.pi * t) - 1) / 2
def EaseInQuad(t):
	return t**2
def EaseOutQuad(t):
	return 1 - (1 - t)**2
def EaseInOutQuad(t):
	return 2*t**2 if t < 0.5 else 1 - (-2*t + 2)**2 / 2
def EaseInCubic(t):
	return t**3
def EaseOutCubic(t):
	return 1 - (1 - t)**3
def EaseInOutCubic(t):
	return 4*t**3 if t < 0.5 else 1 - (-2*t + 2)**3 / 2
def EaseInQuart(t):
	return t**4
def EaseOutQuart(t):
	return 1 - (1 - t)**4
def EaseInOutQuart(t):
	return 8*t**4 if t < 0.5 else 1 - (-2*t + 2)**4 / 2
def EaseInQuint(t):
	return t**5
def EaseOutQuint(t):
	return 1 - (1 - t)**5
def EaseInOutQuint(t):
	return 16*t**5 if t < 0.5 else 1 - (-2*t + 2)**5 / 2
def EaseInExpo(t):
	return 0 if t == 0 else 2**(10 * t - 10)
def EaseOutExpo(t):
	return 1 if t == 1 else 1 - 2**(-10 * t)
def EaseInOutExpo(t):
	return 0 if t == 0 else 1 if t == 1 else 2**(10 *
                                                                   (2*t - 1)) / 2 if t < 0.5 else (2 - 2**(-10 * (2*t - 1))) / 2


def EaseInCirc(t):
	return 1 - math.sqrt(1 - t**2)
def EaseOutCirc(t):
	return math.sqrt(1 - (t - 1)**2)
def EaseInOutCirc(t):
	return (1 - math.sqrt(1 - (2*t)**2)) / \
    2 if t < 0.5 else (math.sqrt(1 - (-2*t + 2)**2) + 1) / 2


def EaseInBack(t):
	return 2.70158*t**3 - 1.70158*t**2
def EaseOutBack(t):
	return 1 + 2.70158*(t - 1)**3 + 1.70158*(t - 1)**2


def EaseInOutBack(t):
	return (2.70158*(2*t)**3 - 1.70158*(2*t)**2) / \
    2 if t < 0.5 else (2 + 2.70158*(-2*t + 2)**3 + 1.70158*(-2*t + 2)**2) / 2


def EaseInElastic(t):
	return 0 if t == 0 else 1 if t == 1 else - \
    (2**(10 * t - 10)) * math.sin((t * 10 - 10.75) * ((2 * math.pi) / 3))


def EaseOutElastic(t):
	return 0 if t == 0 else 1 if t == 1 else 2**(-10 *
                                                                    t) * math.sin((t * 10 - 0.75) * ((2 * math.pi) / 3)) + 1
def EaseInOutElastic(t):
	return 0 if t == 0 else 1 if t == 1 else -(2**(10 * (2*t - 1))) * math.sin((2*t - 1) * 10 - 10.75) * (
    (2 * math.pi) / 3) / 2 if t < 0.5 else 2**(-10 * (2*t - 1)) * math.sin((2*t - 1) * 10 - 0.75) * ((2 * math.pi) / 3) / 2 + 1


def EaseInBounce(t):
	return 1 - (1 - t)**2 * (2 - t)
def EaseOutBounce(t):
	return 1 - (1 - t)**2 * (2 - t)


def EaseInOutBounce(t):
	return 1 - (1 - t)**2 * \
    (2 - t) if t < 0.5 else 1 - (1 - t)**2 * (2 - t)
