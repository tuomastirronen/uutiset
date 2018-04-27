class HomeController < ApplicationController	
  def index  	

    @stocks = Feed.fetch_stock_prices
    @currencies = Feed.fetch_currencies    
    @headlines = Feed.fetch_headlines
    @q = Entry.ransack(params[:q])
    @entries = @q.result.paginate(:page => params[:page], per_page: 10)
    # @entries = Feed.fetch.entries
  	# @sources = Source.all  	
  	
  end
end
