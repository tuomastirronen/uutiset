class HomeController < ApplicationController	
  def index  	
  	session[:sources] = params.except('utf8', '✓', 'commit', 'Päivitä', 'controller', 'home', 'action', 'index').map{|param| param[0]}
  	
  	@feed = NewsDispenser.fetch(session[:sources])  

  	@sources = Source.all

  end
end
