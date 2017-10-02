class HomeController < ApplicationController	
  def index  	
  	clean_params = params.except('utf8', '✓', 'commit', 'Päivitä', 'controller', 'home', 'action', 'index').map{|param| param[0]}
  	unless clean_params.empty? then
  		session[:sources] = clean_params
  	end
  	# @feed = Feed.fetch(session[:sources])
  	
    @stocks = Feed.fetch_stock_prices
    @currencies = Feed.fetch_currencies
    
  	@entries = Entry.where(:click_bait => false).paginate(:page => params[:page])
    # @entries = Feed.fetch(session[:sources]).entries
  	@sources = Source.all  	
  end
end
