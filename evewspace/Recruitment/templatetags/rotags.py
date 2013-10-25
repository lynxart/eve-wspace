from django import template

register = template.Library()

@register.inclusion_tag('render_question.html', takes_context=True)
def render_question(context, question):
    context['question'] = question
    return context

@register.inclusion_tag('render_question.html', takes_context=True)
def render_edit_question(context, question):
    context['question'] = question
    context['edit_mode'] = True
    return context
