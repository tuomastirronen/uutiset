class AddClicksToEntry < ActiveRecord::Migration
  def change
  	add_column :entries, :clicks, :int, :default => 0
  end
end
