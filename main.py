
#main.py
# the import section
import webapp2
import jinja2
import os
from google.appengine.ext import ndb
import time

# This initializes the jinja2 Environment.
# This will be the same in every app that uses the jinja2 templating library.
the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Products(ndb.Model):
  name_of_product = ndb.StringProperty(required=True)
  manufacturer_of_product = ndb.StringProperty(required=True)
  style_of_product= ndb.StringProperty(required=True)
  purchase_price_of_product=ndb.StringProperty(required=True)
  sale_price_of_product=ndb.StringProperty(required=True)
  amount_on_hand_of_product=ndb.StringProperty(required=True)
  commision_of_product=ndb.StringProperty(required=True)

class Salesperson(ndb.Model):
  first_name_s = ndb.StringProperty(required=True)
  last_name_s = ndb.StringProperty(required=True)
  address_s= ndb.StringProperty(required=True)
  phone_s=ndb.FloatProperty(required=True)
  start_date_s=ndb.StringProperty(required=True)
  end_date_s=ndb.StringProperty(required=True)
  manager_s=ndb.StringProperty(required=True)

class Customer(ndb.Model):
    first_name_c = ndb.StringProperty(required=True)
    last_name_c = ndb.StringProperty(required=True)
    address_c= ndb.StringProperty(required=True)
    phone_c=ndb.FloatProperty(required=True)
    start_date_c=ndb.StringProperty(required=True)

# class Sales(ndb.Model):
#   product_sales = ndb.StringProperty(required=True)
#   salesperson_sales = ndb.StringProperty(required=True)
#   customer_sales= ndb.StringProperty(required=True)
#   sale_date=ndb.FloatProperty(required=True)
#
# class Discount(ndb.Model):
#   product_discount = ndb.StringProperty(required=True)
#   start_discount = ndb.StringProperty(required=True)
#   end_discount= ndb.StringProperty(required=True)
#   percent_discount=ndb.FloatProperty(required=True)

class HomePage(webapp2.RequestHandler):
    def get(self):  # for a get request
        home_template = the_jinja_env.get_template('index.html')
        self.response.write(home_template.render())  # the response
class AddProductPage(webapp2.RequestHandler):
    def get(self):  # for a get request
        addProduct_template = the_jinja_env.get_template('html/addProduct.html')
        self.response.write(addProduct_template.render())  # the response
class DisplayProductPage(webapp2.RequestHandler):
    def get(self):  # for a get request
        displayProduct_template = the_jinja_env.get_template('html/productDisplay.html')
        products_all=Products.query().order(Products.name_of_product).fetch()
        self.response.write(displayProduct_template.render({'product_info': products_all,
                                                    }))  # the response
class ShowProduct(webapp2.RequestHandler):
    def post(self):
        results_product_template = the_jinja_env.get_template('html/addProductConfirm.html')
        # Access the user data via the form's input elements' names.
        product_name = self.request.get('nameProductGiven')
        product_manufacturer = self.request.get('manufacturerProductGiven')
        product_style=self.request.get('styleGiven')
        product_purchase_price=self.request.get('purchasePriceGiven')
        product_sale_price=self.request.get('salePriceGiven')
        product_amount=self.request.get('amountProductGiven')
        product_commission=self.request.get('commissionProductGiven')
        # Organize that user data into a dictionary.
        the_variable_product_dict = {
            "name_from_form": product_name,
            "manufacturer_from_form": product_manufacturer,
            "style_from_form": product_style,
            "purchase_price_from_form":product_purchase_price,
            "sale_price_from_form":product_sale_price,
            "amount_from_form":product_amount,
            "commission_from_form":product_commission,
        }
        new_product_entity=Products(name_of_product=product_name, manufacturer_of_product=product_manufacturer, style_of_product=product_style, purchase_price_of_product=product_purchase_price, sale_price_of_product=product_sale_price, amount_on_hand_of_product=product_amount, commision_of_product=product_commission)
        new_product_entity.put()
        print(new_product_entity)
        # pass that dictionary to the Jinja2 `.render()` method
        self.response.write(results_product_template.render(the_variable_product_dict))


# the app configuration section
app = webapp2.WSGIApplication([
    ('/', HomePage), #this maps the root url to the Main Page Handler
    ('/displayProduct', DisplayProductPage),
    ('/addProduct', AddProductPage),
    ('/addProductConfirm', ShowProduct),
], debug=True)
