class Source
	attr_accessor :id
	attr_accessor :name
	attr_accessor :url

	def initialize(id, name, url)
    	@id = id
    	@name = name
		@url = url
	end

	def self.find_by_id(id)
		if id.nil? then
			all
		else
			all.select{|source| id.include?(source.id)}
		end		
	end

	def self.all
		@sources
	end

	@sources = [
		Source.new('hs', 'Helsingin Sanomat', 'http://www.hs.fi/rss/tuoreimmat.xml'),
		Source.new('il', 'Iltalehti', 'http://www.iltalehti.fi/rss/uutiset.xml'),		
		Source.new('is', 'Ilta-Sanomat', 'http://www.is.fi/rss/tuoreimmat.xml'),
		Source.new('kl', 'Kauppalehti', 'https://feeds.kauppalehti.fi/rss/main'),
		Source.new('tivi', 'Tietoviikko', 'http://www.tivi.fi/rss.xml'),
		Source.new('yle', 'YLE', 'https://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_UUTISET')
	]
end