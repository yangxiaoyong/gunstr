class AddTestData < ActiveRecord::Migration
  def self.up
    Product.delete_all
    Product.create(:title => 'Pragmatic Version Control',
                   :description =>
                    %{<p>
                      This is book is recipe-based blalalallalalallala ...
                    </p>},
                  :image_url => '/images/svn.jpg',
                  :price => 28.50)
  end

  def self.down
  end
end
