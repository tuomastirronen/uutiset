class NewsDispenser < ActiveRecord::Base
	require 'httparty'	

	def self.fetch(s)		
		feed = Array.new

		Source.find_by_id(s).each do |source|
			xml = HTTParty.get(source.url).body			
			Feedjira::Feed.parse(xml).entries.each do |entry|				
				feed.push entry
			end
		end

		feed.sort_by { |a| a["published"] }.reverse
	end
end
