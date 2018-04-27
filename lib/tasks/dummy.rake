desc "Write dummy data to database"
task :dummy => :environment do
	500.times { |i| Entry.create(guid: rand(36**8).to_s(36), url: "http://mediaforum.fi", source: "NA", title: "Title #{i}", published: "2018-04-27 07:47:27.272005", summary: "Kalevan mukaan poliisin tietoon tuli viime vuonna lähes 200 rikosilmoitusta kiihottamisesta kansanryhmää vastaan tai sen törkeästä tekomuodosta. Se on lähes neljä kertaa edellisvuotta enemmän.", categories: "Category 1,Category 2" ) }
end