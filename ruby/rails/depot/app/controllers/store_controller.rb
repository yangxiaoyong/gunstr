#---
# Excerpted from "Agile Web Development with Rails, 2nd Ed.",
# published by The Pragmatic Bookshelf.
# Copyrights apply to this code. It may not be used to create training material, 
# courses, books, articles, and the like. Contact us if you are in doubt.
# We make no guarantees that this code is fit for any purpose. 
# Visit http://www.pragmaticprogrammer.com/titles/rails2 for more book information.
#---
class StoreController < ApplicationController
  
  def index
    @products = Product.find_products_for_sale
    @cart = find_cart
  end


  
  def add_to_cart
    begin                     
      product = Product.find(params[:id])  
    rescue ActiveRecord::RecordNotFound
      logger.error("Attempt to access invalid product #{params[:id]}")
      redirect_to_index("Invalid product")
    else
      @cart = find_cart
      @current_item = @cart.add_product(product)
      redirect_to_index unless request.xhr?
    end
  end
  

  def empty_cart
    session[:cart] = nil
    redirect_to_index
  end

  private
  
  def redirect_to_index(msg = nil)
    flash[:notice] = msg if msg
    redirect_to :action => :index
  end
    
  def find_cart
    session[:cart] ||= Cart.new
  end
end
