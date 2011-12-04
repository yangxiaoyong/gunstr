from tornado import template

t = template.Template("<html>{{ my }}</html>")
print t.generate(my="xxx")
