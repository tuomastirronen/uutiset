class Feed	
	require 'httparty'	
	require 'json'	
	require 'openssl'
	require 'open-uri'

	# Returns the feed
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

	# Writes feed entries to database
	def self.write_db(sources)
		if sources.nil?
			sources = Source.all.map { |source| source.id }.to_a
		end
		feed = fetch(sources)
		feed.entries.each do |entry|
			begin
				Entry.create!(
					:guid => entry.entry_id, 
					:source => entry.source, 
					:url => entry.url, 
					:title => entry.title, 
					:summary => entry.summary,
					:published => entry.published,
					:categories => entry.categories.join(","),
					:image => entry.image,
					:click_bait => false
				)
			rescue Exception => e
				puts "#{e}"
			end			
		end
	end

	# Return finance data
	def self.fetch_stock_prices
		url = "https://www.kauppalehti.fi/5/i/porssi/"
	    doc = Nokogiri::HTML(open(url, :ssl_verify_mode => OpenSSL::SSL::VERIFY_NONE))

	    entries = doc.css('div#nousijat_helsinki')[0]

	    data = []

	    entries.children.css('table/tbody/tr').each do |entry|
	    	data.append [
	    		entry.css('td')[0].text,
	    		"#{entry.css('td')[1].text} EUR",
	    		entry.css('td')[2].text
	    	]
	    end	 

	    data.drop(1) # remove headers
	end

	# Return currency data
	def self.fetch_currencies
		base_currency = 'eur'

		currencies = [
			{:currency => 'btc', :name => 'Bitcoin'},
			{:currency => 'eth', :name => 'Ethereum'}
		]
		data = []

		currencies.each do |currency|
			url = "https://www.bitstamp.net/api/v2/ticker/#{currency[:currency]}#{base_currency}"			
			response = JSON.load(open(url, :ssl_verify_mode => OpenSSL::SSL::VERIFY_NONE))
			data.append [
				currency[:name],
				"#{response['last']} EUR"
			]
		end		

		data
	end

	def self.fetch_headlines
		file = File.read "lib/assets/classifier/data/headlines.json"
		data = JSON.parse(file)['headlines']
	end
end
