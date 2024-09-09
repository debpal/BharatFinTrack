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
    
    
    def get_indices_by_category(self, category):
        
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
        
        if category in self.indices_category:
            pass
        else:
            raise Exception(f'Invadid category: {category}')
        
        return indices[category]
    
    
    @property
    def downloadable_indices(self):
        
        '''
        Returns a list of all indices names.
        '''
        
        output = [
            index for category in self.indices_category for index in self.get_indices_by_category(category)
        ]
        
        return output
    

    def is_downloadable_index(self, index):
        
        '''
        Checks whether a specified NSE index name is downloadable.

        Parameters
        ----------
        index : str
            The name of the NSE index.

        Returns
        -------
        bool
            True if the index name is valid, False.
        '''
        
        return index in self.downloadable_indices
    
    
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
            map(lambda x: (x, date_dict.get(x, default_date)), self.downloadable_indices)
        )
        
        return output
    
    
    def get_index_base_date(self, index):
        
        '''
        Returns the base date for a specified NSE index.

        Parameters
        ----------
        index : str
            The name of the NSE index.

        Returns
        -------
        str
            The base date of the index in 'DD-MMM-YYYY' format.
        '''
        
        if self.is_downloadable_index(index):
            pass
        else:
            raise Exception(f'Invalid index: {index}')
        
        return self.indices_base_date[index]
    
    
    def get_index_base_value(self, index):
        
        '''
        Returns the base value for a specified NSE index.

        Parameters
        ----------
        index : str
            The name of the NSE index.

        Returns
        -------
        float
            The base value of the index.
        '''
        
        if self.is_downloadable_index(index):
            pass
        else:
            raise Exception(f'Invalid index: {index}')
            
        base_value = {'NIFTY IT': 100.0}
        
        return base_value.get(index, 1000.0)