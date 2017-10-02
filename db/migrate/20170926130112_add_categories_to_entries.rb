class AddCategoriesToEntries < ActiveRecord::Migration
  def change
  	add_column :entries, :categories, :string
  end
end
