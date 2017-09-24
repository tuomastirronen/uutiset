class Source
	attr_accessor :id
	attr_accessor :name
	attr_accessor :url

	def initialize(id, name, url)
    	@id = id
    	@name = name
		@url = url
	end	

	def self.find(id)
		all.select{|source| id.include?(source.id)}
	end

	def self.find_by_id(id)
		all.select{|source| id.include?(source.id)}
	end

	def self.all
		@sources
	end

	@sources = [
		Source.new('helsingin_sanomat', 'Helsingin Sanomat', 'http://www.hs.fi/rss/tuoreimmat.xml'),
		Source.new('iltalehti', 'Iltalehti', 'http://www.iltalehti.fi/rss/uutiset.xml'),
		Source.new('iltasanomat', 'Ilta-Sanomat', 'http://www.is.fi/rss/tuoreimmat.xml'),
		Source.new('kauppalehti', 'Kauppalehti', 'https://feeds.kauppalehti.fi/rss/main'),
		Source.new('tivi', 'Tietoviikko', 'http://www.tivi.fi/rss.xml')#,
		#Source.new('cnn', 'CNN', 'http://rss.cnn.com/rss/edition.rss')
	]
end