require 'csv'
desc "Write CSV feed to database"
task :import_csv => :environment do    	
  	CSV.foreach("vendor/data.csv", { encoding: "UTF-8", headers: true, header_converters: :symbol, converters: :all}) do |entry|		
		begin			
			Entry.create(
				:guid => entry[0],
				:source => entry[1],
				:url => entry[2],
				:title => entry[3],
				:summary => entry[4],
				:published => entry[5],
				:click_bait => entry[6],
				:cluster => entry[7],
				:created_at => entry[8],
				:updated_at => entry[9],
				:categories => entry[10],
				:image => entry[11],
				:clicks => entry[12]
			)			
		rescue Exception => e
			puts e
		end
	end
end