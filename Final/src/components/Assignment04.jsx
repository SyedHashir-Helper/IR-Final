import React, { useState } from 'react';
import { 
  HomeOutlined, 
  ShoppingOutlined, 
  TagOutlined, 
  RightOutlined 
} from '@ant-design/icons';
import '../styles/Structure.css';

// Mock Data Structure
const categoryData = {
  Electronics: {
    Computers: {
      Laptops: [
        { id: 'lap1', name: 'MacBook Pro', price: '$1999', image: '/api/placeholder/200/200' },
        { id: 'lap2', name: 'Dell XPS', price: '$1299', image: '/api/placeholder/200/200' }
      ],
      Desktops: [
        { id: 'desk1', name: 'iMac', price: '$1499', image: '/api/placeholder/200/200' },
        { id: 'desk2', name: 'HP Pavilion', price: '$799', image: '/api/placeholder/200/200' }
      ]
    },
    Smartphones: {
      Apple: [
        { id: 'phone1', name: 'iPhone 13', price: '$799', image: '/api/placeholder/200/200' },
        { id: 'phone2', name: 'iPhone 13 Pro', price: '$999', image: '/api/placeholder/200/200' }
      ],
      Samsung: [
        { id: 'sam1', name: 'Galaxy S21', price: '$699', image: '/api/placeholder/200/200' },
        { id: 'sam2', name: 'Galaxy Note', price: '$899', image: '/api/placeholder/200/200' }
      ]
    }
  },
  Fashion: {
    MensWear: {
      Shirts: [
        { id: 'shirt1', name: 'Cotton Polo', price: '$49', image: '/api/placeholder/200/200' },
        { id: 'shirt2', name: 'Formal Shirt', price: '$79', image: '/api/placeholder/200/200' }
      ],
      Pants: [
        { id: 'pant1', name: 'Chino Trouser', price: '$59', image: '/api/placeholder/200/200' },
        { id: 'pant2', name: 'Denim Jeans', price: '$89', image: '/api/placeholder/200/200' }
      ]
    }
  }
};

const CategoryNavigation = () => {
  const [currentLevel, setCurrentLevel] = useState({
    category: null,
    subCategory: null,
    subSubCategory: null,
    items: null
  });

  const navigateCategory = (category) => {
    setCurrentLevel({
      category,
      subCategory: null,
      subSubCategory: null,
      items: null
    });
  };

  const navigateSubCategory = (subCategory) => {
    setCurrentLevel(prev => ({
      ...prev,
      subCategory,
      subSubCategory: null,
      items: null
    }));
  };

  const navigateSubSubCategory = (subSubCategory) => {
    setCurrentLevel(prev => ({
      ...prev,
      subSubCategory,
      items: categoryData[prev.category][prev.subCategory][subSubCategory]
    }));
  };

  const renderBreadcrumbs = () => {
    const { category, subCategory, subSubCategory } = currentLevel;
    return (
      <div className="breadcrumb-container">
        <span 
              className="breadcrumb-item"
              onClick={() => navigateCategory(null)}
            >
              <HomeOutlined /> Home
            </span>
            <RightOutlined className="breadcrumb-separator" />
        {category && (
          <>
            
            <span 
              className="breadcrumb-item"
              onClick={() => navigateCategory(category)}
            >
              <ShoppingOutlined /> {category}
            </span>
            {subCategory && (
              <>
                <RightOutlined className="breadcrumb-separator" />
                <span 
                  className="breadcrumb-item"
                  onClick={() => navigateSubCategory(null)}
                >
                  <TagOutlined /> {subCategory}
                </span>
                {subSubCategory && (
                  <>
                    <RightOutlined className="breadcrumb-separator" />
                    <span className="breadcrumb-item active">
                      {subSubCategory}
                    </span>
                  </>
                )}
              </>
            )}
          </>
        )}
      </div>
    );
  };

  const renderContent = () => {
    if (!currentLevel.category) {
      return (
        <div className="category-grid">
          {Object.keys(categoryData).map(category => (
            <div 
              key={category} 
              className="category-card"
              onClick={() => navigateCategory(category)}
            >
              <div className="category-icon">
                <ShoppingOutlined />
              </div>
              <h3>{category}</h3>
            </div>
          ))}
        </div>
      );
    }

    if (!currentLevel.subCategory) {
      return (
        <div className="category-grid">
          {Object.keys(categoryData[currentLevel.category]).map(subCategory => (
            <div 
              key={subCategory} 
              className="category-card"
              onClick={() => navigateSubCategory(subCategory)}
            >
              <div className="category-icon">
                <TagOutlined />
              </div>
              <h3>{subCategory}</h3>
            </div>
          ))}
        </div>
      );
    }

    if (!currentLevel.subSubCategory) {
      return (
        <div className="category-grid">
          {Object.keys(categoryData[currentLevel.category][currentLevel.subCategory]).map(subSubCategory => (
            <div 
              key={subSubCategory} 
              className="category-card"
              onClick={() => navigateSubSubCategory(subSubCategory)}
            >
              <div className="category-icon">
                <TagOutlined />
              </div>
              <h3>{subSubCategory}</h3>
            </div>
          ))}
        </div>
      );
    }

    return (
      <div className="product-grid">
        {currentLevel.items.map(item => (
          <div key={item.id} className="product-card">
            {/* <img src={item.image} alt={item.name} className="product-image" /> */}
            <div className="product-details">
              <h3>{item.name}</h3>
              <p className="product-price">{item.price}</p>
              <button className="product-button">View Details</button>
            </div>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="category-navigation-container">
      {renderBreadcrumbs()}
      {renderContent()}
    </div>
  );
};

export default CategoryNavigation;