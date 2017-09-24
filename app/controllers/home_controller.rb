class HomeController < ApplicationController	
  def index  	
  	clean_params = params.except('utf8', '✓', 'commit', 'Päivitä', 'controller', 'home', 'action', 'index').map{|param| param[0]}
  	unless clean_params.empty? then
  		session[:sources] = clean_params
  	end
  	@feed = Feed.fetch(session[:sources])
  	@sources = Source.all  	
  end
end
