import { render,fireEvent, waitFor, screen } from '@testing-library/react';
import App from './App';
import Board from './Board'

test('removes login after button press', () => {
  const resultRender = render(<App />);
  
  const loginButton= screen.getByText('Login');
  expect(loginButton).toBeInTheDocument();
  
  fireEvent.click(loginButton)
  
  expect(loginButton).not.toBeInTheDocument();
  
  const gameStatus= screen.getByText('The game is in progress');
  expect(gameStatus).toBeInTheDocument();
});

test('restart board', () => {
  const resultRender = render(<Board />);
  
  const restartButton= screen.getByText('Restart Game');
  const xBox = screen.getAllByText('').forEach(node => fireEvent.click(node))
  const xText = screen.getAllByText('X').forEach(node =>expect(node).toBeInTheDocument());
  
  
  fireEvent.click(restartButton)
    
  const nullText = screen.getAllByText('').forEach(node =>expect(node).toBeInTheDocument());
});

test('render leaderBoard after login in and pressing show leaderBoardButton', () => {
  const resultRender = render(<App />);
  
  const loginButton= screen.getByText('Login');
  
  fireEvent.click(loginButton)
  
  const leaderButton= screen.getByText('Show/Hide leaderBoard');
  const preText= screen.getByText('Press button to see scores')
  expect(preText).toBeInTheDocument();
  
  fireEvent.click(leaderButton)
  const leaderText= screen.getByText('score')
  
  expect(leaderText).toBeInTheDocument();
  expect(preText).not.toBeInTheDocument();
});