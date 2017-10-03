desc "Write RSS feed to database"
task :update_feed => :environment do
  puts "Updating feed..."
  Feed.write_db(nil)
  puts "done."
end

desc "Cluster and summarize entries"
task :update_headlines => :environment do
  puts "Clustering..."
  result = `python lib/assets/classifier/clustering.py`
  puts "Summarizing..."
  result = `python lib/assets/classifier/summarization.py`
  puts "done."
end