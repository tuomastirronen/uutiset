class Entry < ActiveRecord::Base
	self.primary_key = 'guid'

	default_scope  { order(:published => :desc) }

	def categories
		self[:categories].split(',')
	end
end
