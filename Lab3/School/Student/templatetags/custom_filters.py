from django import template
register=template.Library()
@register.filter(name="print_name")
def printName(name):
  return("your name is:"+name) 
@register.filter(name="edit_filter")
def edit(name):
  return(name+"Your are In Edit Page ")
@register.filter(name="delete_filter")
def delete(age):
  return("Your are In delete Page Your Age is :",age)
@register.filter(name="show_filter")
def show(degree):
  return("Your degrees  is : {}".format(degree))