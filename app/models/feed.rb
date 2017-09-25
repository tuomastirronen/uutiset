class Feed
	require 'httparty'	
	require 'csv'

	def self.fetch(sources)	
		Feedjira::Feed.add_common_feed_element("source")	
		
		feed = Array.new

		Source.find_by_id(sources).each do |source|
			xml = HTTParty.get(source.url).body
			Feedjira::Feed.parse(xml).entries.take(30).each do |entry|
				entry.source = source.name
				feed.push entry
			end
		end

		feed.sort_by { |a| a["published"] }.reverse
	end

	def self.write_csv(sources)
		feed = fetch(sources)
		
		CSV.open("lib/assets/python/clustering/entries.csv", "w", {:col_sep => "|"}) do |csv|
			feed.entries.each do |entry|
				csv << [entry.title, entry.categories.first, entry.summary]
			end
		end
	end
end
