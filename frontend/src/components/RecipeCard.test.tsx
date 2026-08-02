import { RecipeCard } from '@/components/RecipeCard';
import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

const mockRecipe = {
  id: '11111111-1111-1111-1111-111111111111',
  title: 'にんじんのやわらか煮',
  description: '離乳食後期から食べられる、やわらかく煮たにんじん。',
  category: 'side_dish',
  ingredients: ['にんじん 1本', 'だし汁 適量', 'みりん 少々'],
  instructions: ['にんじんをやわらかくゆでる'],
  cooking_time_minutes: 15,
  servings: 2,
  image_url: null,
  source_url: null,
  tags: ['離乳食', '後期'],
  created_at: '2026-08-01T00:00:00Z',
  is_public: true,
};

describe('RecipeCard', () => {
  it('renders the recipe title', () => {
    render(<RecipeCard recipe={mockRecipe} />);
    expect(screen.getByText('にんじんのやわらか煮')).toBeInTheDocument();
  });

  it('renders the category label in Japanese', () => {
    render(<RecipeCard recipe={mockRecipe} />);
    expect(screen.getByText('副菜')).toBeInTheDocument();
  });

  it('renders cooking time', () => {
    render(<RecipeCard recipe={mockRecipe} />);
    expect(screen.getByText('15分')).toBeInTheDocument();
  });

  it('renders description', () => {
    render(<RecipeCard recipe={mockRecipe} />);
    expect(
      screen.getByText('離乳食後期から食べられる、やわらかく煮たにんじん。')
    ).toBeInTheDocument();
  });

  it('links to the recipe detail page', () => {
    render(<RecipeCard recipe={mockRecipe} />);
    const link = screen.getByRole('link');
    expect(link).toHaveAttribute('href', `/recipes/${mockRecipe.id}`);
  });

  it('renders ingredient tags', () => {
    render(<RecipeCard recipe={mockRecipe} />);
    expect(screen.getByText('にんじん 1本')).toBeInTheDocument();
    expect(screen.getByText('だし汁 適量')).toBeInTheDocument();
  });

  it('renders the extra ingredient count when there are more than 3', () => {
    const recipeWithMany = {
      ...mockRecipe,
      ingredients: ['にんじん', 'たまねぎ', 'じゃがいも', 'だし汁', 'しょうゆ'],
    };
    render(<RecipeCard recipe={recipeWithMany} />);
    expect(screen.getByText('+2個')).toBeInTheDocument();
  });
});
