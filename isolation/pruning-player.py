class PruningAlphaBetaPlayer(AlphaBetaPlayer):

    def alphabeta_with_score(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        #print('####minimax### @ ',depth)
        self.seenBoards = {}
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        moves = game.get_legal_moves()
        mval = float("-inf")
        best_move = None
        for move in moves:
            moved = game.forecast_move(move)
            seenVal = self.getSeenBoard(moved)
            if seenVal:
                print('Was able to prune',moved)
                nval = seenVal
            else:
                nval = self.minvalue(moved,depth-1,alpha,beta)
                self.setSeenBoard(moved,nval)
            if not best_move: best_move = move
            if nval > mval:
                mval = nval
                best_move = move
            if nval >= beta: return mval, best_move
            alpha = max(alpha,nval)
        return mval,best_move


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        return self.alpha_beta_with_score(game, depth, alpha, beta)

    def getSeenBoard(self,board):
        if board in self.seenBoards:
            return self.seenBoards.get(board)
        r1 = board.rotate90()
        if r1 in self.seenBoards:
            return self.seenBoards.get(r1)
        r2 = r1.rotate90()
        if r2 in self.seenBoards:
            return self.seenBoards.get(r2)
        r3 = r2.rotate90()
        if r3 in self.seenBoards:
            return self.seenBoards.get(r3)
        fx = board.flipX()
        if fx in self.seenBoards:
            return self.seenBoards.get(fx)
        fy = board.flipY()
        if fy in self.seenBoards:
            return self.seenBoards.get(fy)
        fd = board.flip_diag_positive()
        if fy in self.seenBoards:
            fnd = board.flip_diag_negative()
        if fy in self.seenBoards:
            return self.seenBoards.get(fnd)
        return None


    def setSeenBoard(self,board, val):
        self.seenBoards[board] = val

    def maxvalue(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        moves = game.get_legal_moves()
        if self.terminal_test(game,moves,depth):
            score = self.score(game,self)
            #print('-'*(self.search_depth - depth) ,'max',score)
            return score
        mval = float("-inf")
        for move in moves:
            moved = game.forecast_move(move)
            seenVal = self.getSeenBoard(moved)
            if seenVal:
                print('Was able to prune',moved)
                nval = seenVal
            else:
                nval = self.minvalue(moved,depth-1,alpha,beta)
                self.setSeenBoard(moved,nval)
            if nval > mval:
                mval = nval
            if nval >= beta: return mval
            alpha = max(alpha,nval)
        return mval

    def minvalue(self,game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        moves = game.get_legal_moves()
        if self.terminal_test(game,moves,depth):
          score = self.score(game,self)
          #print('-'*(self.search_depth - depth) ,'min',score)
          return score
        mval = float("inf")
        for move in moves:
            moved = game.forecast_move(move)
            seenVal = self.getSeenBoard(moved)
            if seenVal:
                nval = seenVal
            else:
                nval = self.maxvalue(moved,depth-1,alpha,beta)
                self.setSeenBoard(moved,nval)
            if nval < mval:
                mval = nval
            if nval <= alpha: return mval
            beta = min(beta,nval)
        return mval

    def terminal_test(self, game, moves, depth):
        if depth <= 0: return True
        return len(moves) <= 0
