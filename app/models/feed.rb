class Feed < ActiveRecord::Base
	require 'httparty'	

	def self.fetch(s)	
		Feedjira::Feed.add_common_feed_element("source")	
		feed = Array.new

		Source.find_by_id(s).each do |source|
			xml = HTTParty.get(source.url).body
			Feedjira::Feed.parse(xml).entries.each do |entry|
				puts entry
				entry.source = source.name
				feed.push entry
			end
		end

		feed.sort_by { |a| a["published"].to_date }.reverse
	end
end
