class HomeController < ApplicationController	
  def index  	

    @stocks = Feed.fetch_stock_prices
    @currencies = Feed.fetch_currencies    
    @headlines = Feed.fetch_headlines
    @entries = Entry.where(:click_bait => false).paginate(:page => params[:page])
    # @entries = Feed.fetch.entries

  	# @sources = Source.all  	
  end
end
