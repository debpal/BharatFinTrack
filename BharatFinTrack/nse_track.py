class NSETrack:
    
    '''
    Represents characteristics of NSE finance products.
    '''
    
    
    @property
    def indices_category(self):
        
        '''
        Returns a list categories for NSE indices.
        '''
        
        output = [
            'broad', 
            'sectoral', 
            'thematic', 
            'strategy'
        ]
        
        return output
    
    
    def indices_name(self, category):
        
        '''
        Returns NSE indices for a specified category.

        Parameters
        ----------
        category : str
            The classification type of NSE indices.

        Returns
        -------
        list
            A list containing the names of indices for the specified category.
        '''
        
        indices = {}
        
        # broad index
        indices['broad'] = [
            'NIFTY 500',
            'NIFTY 50'
        ]
        
        # sectoral index
        indices['sectoral'] = [
            'NIFTY IT',
            'NIFTY BANK'
        ]
        
        # thematic index
        indices['thematic'] = [
            'NIFTY EV & NEW AGE AUTOMOTIVE',
            'NIFTY INDIA DEFENCE'
        ]
        
        # strategy index
        indices['strategy'] = [
            'NIFTY ALPHA 50',
            'NIFTY MIDCAP150 MOMENTUM 50'
        ]
        
        if category not in self.indices_category:
            raise Exception('Input must be one of {}'.format(self.indices_category))
        else:
            pass
        
        return indices[category]
    
    
    @property
    def indices_all(self):
        
        '''
        Returns a list of all indices names.
        '''
        
        output = [j for i in self.indices_category for j in self.indices_name(i)]
        
        return output
    
    
    @property
    def indices_base_date(self):
        
        '''
        Returns a dictionary where keys are indices 
        and values are their corresponding base dates.
        '''
        
        default_date = '01-Apr-2005'
        
        start_date = {}
        
        start_date['01-Jan-1995'] = ['NIFTY 500']
        start_date['03-Nov-1995'] = ['NIFTY 50']
        start_date['01-Jan-1996'] = ['NIFTY IT']
        start_date['01-Jan-2000'] = ['NIFTY BANK']
        start_date['31-Dec-2003'] = ['NIFTY ALPHA']
        start_date['02-Apr-2018'] = [
            'NIFTY EV & NEW AGE AUTOMOTIVE'
            'NIFTY INDIA DEFENCE'
        ]

        date_dict = {v: key for key, value in start_date.items() for v in value}
        
        output = dict(
            map(lambda x: (x, date_dict.get(x, default_date)), self.indices_all)
        )
        
        return output
