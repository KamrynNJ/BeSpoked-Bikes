
#main.py
# the import section
import webapp2
import jinja2
import os
from google.appengine.ext import ndb
import time
import datetime
from datetime import timedelta

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
  phone_s=ndb.StringProperty(required=True)
  start_date_s=ndb.DateProperty(required=True)
  end_date_s=ndb.DateProperty(required=False)
  manager_s=ndb.StringProperty(required=True)

class Customer(ndb.Model):
    first_name_c = ndb.StringProperty(required=True)
    last_name_c = ndb.StringProperty(required=True)
    address_c= ndb.StringProperty(required=True)
    phone_c=ndb.StringProperty(required=True)
    start_date_c=ndb.DateProperty(required=True)

class Sales(ndb.Model):
  product_sales = ndb.StructuredProperty(Products, repeated=False)
  salesperson_sales = ndb.StructuredProperty(Salesperson, repeated=False)
  customer_sales= ndb.StructuredProperty(Customer, repeated=False)
  commission_amount=ndb.StringProperty(required=True)
  date_sale=ndb.DateProperty(required=True)

class QuarterlyReports(ndb.Model):
  start_date_report=ndb.DateProperty(required=True)
  end_date_report=ndb.DateProperty(required=True)
  creation_report=ndb.DateTimeProperty(required=True)

class CommissionTotals(ndb.Model):
  commission_saleperson=ndb.StructuredProperty(Salesperson, repeated=False)
  total_sale_amount=ndb.FloatProperty(required=True)
  total_commission_amount=ndb.FloatProperty(required=True)

# global dates_start;
# global dates_end;
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
class AddSalespersonPage(webapp2.RequestHandler):
    def get(self):  # for a get request
        addSalesperson_template = the_jinja_env.get_template('html/addSalesperson.html')
        self.response.write(addSalesperson_template.render())  # the response
class DisplaySalespersonPage(webapp2.RequestHandler):
    def get(self):  # for a get request
        displaySalesperson_template = the_jinja_env.get_template('html/salespersonDisplay.html')
        salesperson_all=Salesperson.query().order(Salesperson.last_name_s).fetch()
        self.response.write(displaySalesperson_template.render({'salesperson_info': salesperson_all,
                                                    }))  # the response
class AddCustomerPage(webapp2.RequestHandler):
    def get(self):  # for a get request
        addCustomer_template = the_jinja_env.get_template('html/addCustomer.html')
        self.response.write(addCustomer_template.render())  # the response
class DisplayCustomerPage(webapp2.RequestHandler):
    def get(self):  # for a get request
        displayCustomer_template = the_jinja_env.get_template('html/customerDisplay.html')
        customer_all=Customer.query().order(Customer.last_name_c).fetch()
        self.response.write(displayCustomer_template.render({'customer_info':  customer_all,
                                                    }))  # the response
class DisplaySalePage(webapp2.RequestHandler):
    def get(self):  # for a get request
        display_sale_template = the_jinja_env.get_template('html/saleDisplay.html')
        sale_all=Sales.query().order(Sales.salesperson_sales.last_name_s).fetch()
        self.response.write(display_sale_template.render({'sale_info': sale_all,
                                                    }))  # the response
class AddSalePage(webapp2.RequestHandler):
    def get(self):  # for a get request
        add_Sale_template = the_jinja_env.get_template('html/addSale.html')
        products_all=Products.query().order(Products.name_of_product).fetch()
        customer_all=Customer.query().order(Customer.first_name_c).fetch()
        salesperson_all=Salesperson.query().order(Salesperson.first_name_s).fetch()
        self.response.write(add_Sale_template.render({'product_info': products_all,
                                                      'customer_info': customer_all,
                                                      'saleperson_info': salesperson_all,
                                                    }))  # the response
class AddQuarterlyReportPage(webapp2.RequestHandler):
    def get(self):  # for a get request
        addReport_template = the_jinja_env.get_template('html/addQuartlyReport.html')
        self.response.write(addReport_template.render())  # the response

class DisplayQuarterlyReportPage(webapp2.RequestHandler):
    def get(self):  # for a get request
        display_report_template = the_jinja_env.get_template('html/quartlyReportDisplay.html')

        one_min_earlier=datetime.datetime.now() - timedelta(seconds=20)
        wanted_report_entity=QuarterlyReports.query().filter(QuarterlyReports.creation_report>one_min_earlier).get()

        sales_after_start=Sales.query().filter(Sales.date_sale>=wanted_report_entity.start_date_report).get()
        sales_btw_dates=Sales.query().filter(Sales.date_sale>=wanted_report_entity.start_date_report,Sales.date_sale<=wanted_report_entity.end_date_report)

        sale_filtered=sales_btw_dates
        self.response.write(display_report_template.render({'report_info': sale_filtered,
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

class ShowSalesperson(webapp2.RequestHandler):
    def post(self):
        results_salesperson_template = the_jinja_env.get_template('html/addSalespersonConfirm.html')
        # Access the user data via the form's input elements' names.
        salesperson_first_name = self.request.get('firstNameGiven')
        salesperson_last_name = self.request.get('lastNameGiven')
        salesperson_address=self.request.get('addressGiven')
        salesperson_phone=self.request.get('phoneGiven')
        salesperson_start_date=self.request.get('StartDateGiven')
        salesperson_end_date=self.request.get('EndDateGiven')
        salesperson_manager=self.request.get('managerGiven')

        str_start_date=str(salesperson_start_date)
        saleperson_date_conversion_start=datetime.datetime.strptime(str_start_date, "%Y-%m-%d").date()

        str_end_date=str(salesperson_end_date)
        if(str_end_date==""):
            saleperson_date_conversion_end=None
        else:
            saleperson_date_conversion_end=datetime.datetime.strptime(str_end_date, "%Y-%m-%d").date()
        # Organize that user data into a dictionary.
        the_variable_salesperson_dict = {
            "first_name_from_form": salesperson_first_name,
            "last_name_from_form": salesperson_last_name,
            "address_from_form": salesperson_address,
            "phone_from_form":salesperson_phone,
            "start_date_from_form":saleperson_date_conversion_start,
            "end_date_from_form":saleperson_date_conversion_end,
            "manager_from_form":salesperson_manager,
        }
        new_salesperson_template=Salesperson(first_name_s=salesperson_first_name, last_name_s=salesperson_last_name, address_s=salesperson_address, phone_s=salesperson_phone, start_date_s=saleperson_date_conversion_start, end_date_s=saleperson_date_conversion_end, manager_s=salesperson_manager)
        new_salesperson_template.put()
        print(new_salesperson_template)
        # pass that dictionary to the Jinja2 `.render()` method
        self.response.write(results_salesperson_template.render(the_variable_salesperson_dict))

class ShowCustomer(webapp2.RequestHandler):
    def post(self):
        results_customer_template = the_jinja_env.get_template('html/addCustomerConfirm.html')
        # Access the user data via the form's input elements' names.
        customer_first_name = self.request.get('firstNameGivenC')
        customer_last_name = self.request.get('lastNameGivenC')
        customer_address=self.request.get('addressGivenC')
        customer_phone=self.request.get('phoneGivenC')
        customer_start_date=self.request.get('StartDateGivenC')

        str_date=str(customer_start_date)
        customer_date_conversion=datetime.datetime.strptime(str_date, "%Y-%m-%d").date()
        # Organize that user data into a dictionary.
        the_variable_customer_dict = {
            "c_first_name_from_form": customer_first_name,
            "c_last_name_from_form": customer_last_name,
            "c_address_from_form": customer_address,
            "c_phone_from_form":customer_phone,
            "c_start_date_from_form":customer_date_conversion,
        }
        new_customer_template=Customer(first_name_c=customer_first_name, last_name_c=customer_last_name, address_c=customer_address, phone_c=customer_phone, start_date_c=customer_date_conversion)
        new_customer_template.put()
        print(new_customer_template)
        # pass that dictionary to the Jinja2 `.render()` method
        self.response.write(results_customer_template.render(the_variable_customer_dict))

class ShowSale(webapp2.RequestHandler):
    def post(self):
        results_sale_template = the_jinja_env.get_template('html/addSaleConfirm.html')
        # Access the user data via the form's input elements' names.
        sale_saleperson_given = self.request.get('salesperson')
        sale_customer_given = self.request.get('customer')
        sale_product_given=self.request.get('product')
        sale_start_date_given=self.request.get('startDateSaleGiven')

        sale_str_date=str(sale_start_date_given)
        sale_date_conversion=datetime.datetime.strptime(sale_str_date, "%Y-%m-%d").date()

        chosen_saleperson= Salesperson.query().filter(Salesperson.phone_s == sale_saleperson_given).get()
        chosen_customer= Customer.query().filter(Customer.phone_c == sale_customer_given).get()
        chosen_product= Products.query().filter(Products.name_of_product == sale_product_given).get()

        commission_made=float(chosen_product.purchase_price_of_product)*float(chosen_product.commision_of_product)
        commission_made_str=str(commission_made)
        # Organize that user data into a dictionary.
        the_variable_customer_dict = {
            "saleperson_from_form": chosen_saleperson,
            "customer_from_form": chosen_customer,
            "product_from_form": chosen_product,
            "start_date_from_form":sale_date_conversion,
        }
        new_sale_template=Sales(product_sales=chosen_product, customer_sales=chosen_customer, salesperson_sales=chosen_saleperson, date_sale=sale_date_conversion,commission_amount=commission_made_str)
        new_sale_template.put()

        # pass that dictionary to the Jinja2 `.render()` method
        self.response.write(results_sale_template.render(the_variable_customer_dict))

class ShowQuarterlyReport(webapp2.RequestHandler):
    def post(self):
        results_report_template = the_jinja_env.get_template('html/addQuarterlyReportConfirm.html')
        # Access the user data via the form's input elements' names.
        report_start_date = self.request.get('startDateSearchGiven')
        report_end_date = self.request.get('endDateSearchGiven')

        date_format_report_start=datetime.datetime.strptime(report_start_date, "%Y-%m-%d").date()
        date_format_report_end=datetime.datetime.strptime(report_end_date, "%Y-%m-%d").date()
        report_created=datetime.datetime.now()

        # dates_start=date_format_report_start
        # dates_end=date_format_report_end
        # Organize that user data into a dictionary.
        the_variable_salesperson_dict = {
            "start_date_from_form":date_format_report_start,
            "end_date_from_form":date_format_report_end,
        }

        new_report_template=QuarterlyReports(start_date_report=date_format_report_start, end_date_report=date_format_report_end, creation_report=report_created)
        new_report_template.put()
        # pass that dictionary to the Jinja2 `.render()` method
        self.response.write(results_report_template.render(the_variable_salesperson_dict))

class EditProduct(webapp2.RequestHandler):
    def post(self):
        edit_product_template = the_jinja_env.get_template('html/editProduct.html')
        product_for_editing = self.request.get('hiddenProductValueForEdit')
        The_product_entitity_chosen= Products.query().filter(Products.name_of_product == product_for_editing).get()
        The_product_entitity_chosen_name=The_product_entitity_chosen.name_of_product
        The_product_entitity_chosen_manufacturer=The_product_entitity_chosen.manufacturer_of_product
        The_product_entitity_chosen_style=The_product_entitity_chosen.style_of_product
        The_product_entitity_chosen_purchase_price=The_product_entitity_chosen.purchase_price_of_product
        The_product_entitity_chosen_sale_price=The_product_entitity_chosen.sale_price_of_product
        The_product_entitity_chosen_amount=The_product_entitity_chosen.amount_on_hand_of_product
        The_product_entitity_chosen_commission=The_product_entitity_chosen.commision_of_product
        the_variables_for_edit = {
            "value_from_form_for_edit": The_product_entitity_chosen,
        }

        self.response.write(edit_product_template.render(the_variables_for_edit))
class EditProductConfirm(webapp2.RequestHandler):
    def post(self):
        editProductConfirm_template = the_jinja_env.get_template('html/editProductConfirm.html')
        name_for_it=self.request.get('hiddenProductDateValueForEditing')
        name_editing = self.request.get('nameProductEditing')
        manufacturer_editing=self.request.get('manufacturerProductEditing')
        style_editing=self.request.get('styleEditing')
        purchase_price_editing=self.request.get('purchasePriceProductEditing')
        sale_price_editing=self.request.get('salePriceProductEditing')
        amount_editing=self.request.get('amountEditing')
        commission_editing=self.request.get('commissionEditing')

        The_product_chosen= Products.query().filter(Products.name_of_product ==name_for_it).get()
        The_product_chosen.name_of_product=name_editing
        The_product_chosen.manufacturer_of_product=manufacturer_editing
        The_product_chosen.style_of_product=style_editing
        The_product_chosen.purchase_price_of_product=purchase_price_editing
        The_product_chosen.sale_price_of_product=sale_price_editing
        The_product_chosen.amount_on_hand_of_product=amount_editing
        The_product_chosen.commision_of_product=commission_editing
        The_product_chosen.put()
        print("This is the webtoon")
        print(name_for_it)

        the_variable_for_edit = {
            "editing_name": name_editing,
            "editing_manufacturer": manufacturer_editing,
            "editing_style": style_editing,
            "editing_purchase_price": purchase_price_editing,
            "editing_sale_price": sale_price_editing,
            "editing_amount": amount_editing,
            "editing_commission": commission_editing,
        }


        self.response.write(editProductConfirm_template.render(the_variable_for_edit))

class EditSaleperson(webapp2.RequestHandler):
    def post(self):
        edit_saleperson_template = the_jinja_env.get_template('html/editSaleperson.html')
        saleperson_for_editing = self.request.get('hiddenSalepersonValueForEdit')
        The_saleperson_entitity_chosen= Salesperson.query().filter(Salesperson.phone_s == saleperson_for_editing).get()
        The_saleperson_entitity_chosen_first_name=The_saleperson_entitity_chosen.first_name_s
        The_saleperson_entitity_chosen_last_name=The_saleperson_entitity_chosen.last_name_s
        The_saleperson_entitity_chosen_address=The_saleperson_entitity_chosen.address_s
        The_saleperson_entitity_chosen_phone=The_saleperson_entitity_chosen.phone_s
        The_saleperson_entitity_chosen_start_date=The_saleperson_entitity_chosen.start_date_s
        The_saleperson_entitity_chosen_end_date=The_saleperson_entitity_chosen.end_date_s
        The_saleperson_entitity_chosen_manager=The_saleperson_entitity_chosen.manager_s

        the_variables_for_edit = {
            "value_from_form_for_edit": The_saleperson_entitity_chosen,
        }

        self.response.write(edit_saleperson_template.render(the_variables_for_edit))
class EditSalepersonConfirm(webapp2.RequestHandler):
    def post(self):
        editSalepersonConfirm_template = the_jinja_env.get_template('html/editSalepersonConfirm.html')
        name_for_it=self.request.get('hiddenSalepersonDateValueForEditing')
        first_name_editing = self.request.get('firstNameEditing')
        last_name_editing=self.request.get('lastNameEditing')
        address_editing=self.request.get('addressEditing')
        phone_editing=self.request.get('phoneEditing')
        start_date_editing=self.request.get('startDateEditing')
        end_date_editing=self.request.get('endDateEditing')
        manager_editing=self.request.get('managerEditing')

        str_date=str(start_date_editing)
        saleperson_date_conversion_start=datetime.datetime.strptime(str_date, "%Y-%m-%d").date()

        str_end_date=str(end_date_editing)

        if(str_end_date==""):
            saleperson_date_conversion_end=None
        else:
            saleperson_date_conversion_end=datetime.datetime.strptime(str_end_date, "%Y-%m-%d").date()


        The_product_chosen= Salesperson.query().filter(Salesperson.phone_s ==name_for_it).get()
        The_product_chosen.first_name_s=first_name_editing
        The_product_chosen.last_name_s=last_name_editing
        The_product_chosen.address_s=address_editing
        The_product_chosen.phone_s=phone_editing
        The_product_chosen.start_date_s=saleperson_date_conversion_start
        The_product_chosen.end_date_s=saleperson_date_conversion_end
        The_product_chosen.manager_s=manager_editing


        The_product_chosen.put()
        print("This is the webtoon")
        print(name_for_it)

        the_variable_for_edit = {
            "editing_first_name": first_name_editing,
            "editing_last_name": last_name_editing,
            "editing_address": address_editing,
            "editing_phone": phone_editing,
            "editing_start_date": start_date_editing,
            "editing_end_date": end_date_editing,
            "editing_manager": manager_editing,
        }


        self.response.write(editSalepersonConfirm_template.render(the_variable_for_edit))
# the app configuration section
app = webapp2.WSGIApplication([
    ('/', HomePage), #this maps the root url to the Main Page Handler
    ('/displayProduct', DisplayProductPage),
    ('/addProduct', AddProductPage),
    ('/addProductConfirm', ShowProduct),
    ('/displaySalesperson', DisplaySalespersonPage),
    ('/addSalesperson', AddSalespersonPage),
    ('/addSalespersonConfirm', ShowSalesperson),
    ('/displayCustomer', DisplayCustomerPage),
    ('/addCustomer', AddCustomerPage),
    ('/addCustomerConfirm', ShowCustomer),
    ('/displaySale', DisplaySalePage),
    ('/addSale',AddSalePage),
    ('/addSaleConfirm', ShowSale),
    ('/displayReport', DisplayQuarterlyReportPage),
    ('/addquarterlyReport',AddQuarterlyReportPage),
    ('/addReportConfirm', ShowQuarterlyReport),
    ('/editProduct', EditProduct),
    ('/editProductConfirm', EditProductConfirm),
    ('/editSaleperson', EditSaleperson),
    ('/editSalepersonConfirm', EditSalepersonConfirm),
], debug=True)
