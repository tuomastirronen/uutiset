class Entry < ActiveRecord::Base
	self.primary_key = 'guid'

	default_scope  { order(:published => :desc) }

	def categories
		self[:categories].split(',')
	end

	def click
		self.clicks += 1
		self.save
	end
end
