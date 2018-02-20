"""
Kathryn Egan
"""
import functools


@functools.total_ordering
class Donor:

    def __init__(self, name, *donations):
        """ Initializes Donor object with given name and
        list of donations. Will not accept donations <= 0.
        Will raise ValueError if there are no donations > 0
        in arguments.
        Args:
            name (str) : name of donor
            donations (args) : donations as arguments
        """
        self._name = self.clean_name(name)
        self._donations = self.intake_donations(*donations)
        if not self._donations:
            raise ValueError(
                '{} must have at least one donation > 0'.format(self._name))

    @property
    def name(self):
        """ Returns name of donor.
        Returns:
            str : name of donor
        """
        return self._name

    @property
    def total(self):
        """ Returns total donated.
        Returns:
            float : total donated
        """
        return sum(self.donations)

    @property
    def num(self):
        """ Returns number of donations made.
        Returns:
            int : number of donations made
        """
        return len(self.donations)

    @property
    def average(self):
        """ Returns average donation.
        Returns:
            float : average donation
        """
        return self.total / self.num

    @property
    def donations(self):
        """ Returns donations for this donor.
        Returns:
            list : list of donations
        """
        return self._donations

    @donations.setter
    def donations(self, donations):
        """ Sets donations.
        Args:
            donations (args) : donations as arguments
        """
        self._donations = self.intake_donations(*donations)

    @name.setter
    def name(self, name):
        """ Sets donor name.
        Args:
            name (str) : donor name
        """
        self._name = self.clean_name(name)

    @staticmethod
    def clean_name(name):
        """ Cleans given name.
        Args:
            name (str) : donor name
        Returns:
            str : cleaned name
        """
        return ' '.join(name.split()).title()

    @staticmethod
    def intake_donations(*donations):
        """ Processes given donations and returns
        list of donations that are number > 0
        Args:
            donations (args) : donations as arguments
        Returns:
            list : donations > 0 as list
        """
        processed = []
        for item in donations:
            try:
                item = float(item)
            except ValueError:
                pass
            else:
                if item > 0:
                    processed.append(item)
        return processed

    def thank(self, all_donations=False):
        """ Returns personalized thank you message for this donor.
        Thanks donor for all donations if all_donations is True.
        Args:
            all_donations (bool) : thank donor for all donations
        Returns:
            str : thank you message for donor
        """
        num = self.num if all_donations else 1
        first = self.donations[:-1] if all_donations else []
        rest = self.donations[-1]
        substrings = {
            'donor': self.name,
            's': 's' if num > 1 else '',
            'and': ' and ' if num > 1 else '',
            'first': ', '.join(['${:,.2f}'.format(d) for d in first]),
            'rest': '${:,.2f}'.format(rest),
            'totalling':
                '' if num < 2 else
                ', totalling {}{},'.format(
                    'an incredible ' if self.total > 500
                    else '', '${:,.2f}'.format(self.total))}
        message = \
            'Dear {donor},\nThank you for your generous gift{s} of ' +\
            '{first}{and}{rest}. Your donation{s}{totalling} will ' +\
            'go towards feeding homeless kittens in Seattle. ' +\
            'From the bottom of our hearts, we at Miuvenile Care thank you.' +\
            '\n\nRegards,\nBungelina Bigglesnorf\nChairwoman, Miuvenile Care'
        return message.format(**substrings)

    def add(self, *donations):
        """ Adds passed donations to this donor.
        Args:
            donations (args) : donations as arguments
        """
        donations = self.intake_donations(*donations)
        self._donations.extend(donations)

    def __str__(self):
        """ Returns this donor as a string.
        Returns:
            str : donor as string
        """
        donations = ', '.join([
            '${:,.2f}'.format(d) for d in self.donations])
        return '{}: {}'.format(self.name, donations)

    def __repr__(self):
        """ Returns representation of this donor.
        Returns:
            str : representation of this donor
        """
        donations = ', '.join([
            str(d) for d in self.donations])
        return 'Donor("{}", {})'.format(self.name, donations)

    def __eq__(self, other):
        """ Returns whether this donor is equal to other in
        both name and all donations.
        Args:
            other (Donor) : donor to compare
        Returns:
            bool : True if other donor is equal to this donor
        """
        return (
            self.name == other.name and
            self.donations == other.donations)

    def __lt__(self, other):
        """ Returns whether this donor is less than
        other. Compares name and donations.
        Args:
            other (Donor) : donor to compare
        Returns:
            bool : True if this donor is less than other
        """
        return (
            self.name < other.name and
            self.donations < other.donations)

    def __contains__(self, donation):
        """ Returns whether given donation amount
        has been donated by this donor.
        Args:
            donation (int or float) : donation to search for
        Returns:
            bool :
                True if donation is in donation list
                False otherwise
        """
        return donation in self.donations

    def multiply(self, factor, min_donation=None, max_donation=None):
        donations = map(lambda d: self.apply_factor(
            d, factor, min_donation, max_donation), self.donations)
        return Donor(self.name, *donations)

    @staticmethod
    def apply_factor(d, factor, min_donation, max_donation):
        within_min = True if min_donation is None else d >= min_donation
        within_max = True if max_donation is None else d <= max_donation
        return d * factor if within_min and within_max else d
