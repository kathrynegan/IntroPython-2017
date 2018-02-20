"""
Kathryn Egan
"""
import functools


@functools.total_ordering
class DonorList:

    def __init__(self, *donors):
        """ Initializes list of donors.
        Args:
            donors (args) : donors as arguments
        """
        self._donors = [donor for donor in donors]

    @classmethod
    def from_dictionary(cls, dict):
        """ Returns DonorList from given dictionary.
        Args:
            dict (dic str: list) :
                dictionary of donor names mapped to donations as list
        Returns:
            DonorList : dictionary as DonorList object
        """
        donors = [Donor(name, *donations) for name, donations in dict.items()]
        return cls(*donors)

    @classmethod
    def read_from(cls, filein):
        """ Returns DonorList from given TextIOWrapper object.
        Args:
            filein (TextIOWrapper) : open file
        Returns:
            DonorList : file contents as DonorList object
        """
        donors = []
        for line in filein.readlines():
            line = line.split(',')
            try:
                name = line[0].strip()
            except IndexError:
                continue
            else:
                str_donations = [
                    item.strip().strip('$') for item in line[1:]]
            donations = []
            for d in str_donations:
                try:
                    d = float(d)
                except TypeError:
                    continue
                donations.append(d)
            donors.append(Donor(name, *donations))
        return cls(*donors)

    @property
    def donor_names(self):
        """ Returns donor names as list.
        Returns:
            list of str : list of donor names
        """
        return [donor.name for donor in self.donors]

    @property
    def donors(self):
        """ Returns donors.
        Returns:
            list : list of donors
        """
        return self._donors

    @donors.setter
    def donors(self, donors):
        """ Sets donor list to given donors.
        Args:
            donors (list) : list of donors
        """
        self._donors = donors

    def add(self, donor):
        """ Adds given donor to donor list.
        Args:
            donor (Donor) : donor to add to donor list
        """
        self._donors.append(donor)

    def sort_by(self, key, low_to_high=False):
        """ Returns new DonorList sorted by given key.
        Keys may be one of total, average, or num. Sort
        from low to high if keyword low_to_high is True.
        Args:
            low_to_high (bool) : sort low to high
        Returns:
            DonorList : new DonorList sorted by given key
        """
        functions = {
            'total': lambda donor: donor.total,
            'average': lambda donor: donor.average,
            'num': lambda donor: donor.num}
        if key not in functions:
            raise KeyError('Invalid argument {}'.format(key))
        return DonorList(*sorted(
            self.donors, key=functions[key], reverse=not low_to_high))

    def __getitem__(self, name):
        """ Returns Donor object matching given name.
        Raises ValueError if donor with given name
        does not exist.
        Args:
            name (str) : name to search for
        Returns:
            Donor : donor with name matching given name
        """
        name = Donor.clean_name(name)
        for donor in self.donors:
            if donor.name == name:
                return donor
        raise KeyError('{} not found'.format(name))

    def update(self, donor):
        """ Updates list with given donor. If donor
        with matching name exists, adds given donations
        to existing donor. Otherwise, adds donor.
        Args:
            donor (Donor) : donor to update or add to list
        """
        for d in self.donors:
            if d.name == donor.name:
                d.add(*donor.donations)
                return True
        self.add(donor)

    def __len__(self):
        """ Returns number of donors.
        Returns:
            int : number of donors
        """
        return len(self.donors)

    def __contains__(self, donor):
        """ Returns whether donor list contains
        given donor. If given donor is a Donor
        object, compares name and donations.
        If given donor is a str object, compares
        name only.
        Args:
            donor (Donor or str) : Donor object or donor name
        Returns:
            bool :
                True if given donor or donor name is in donor list
                False otherwise
        """
        for d in self.donors:
            if hasattr(donor, 'name'):
                if d == donor:
                    return True
            elif d.name == donor:
                return True
        return False

    def __iter__(self):
        """ Provides iterator over donor list. """
        for donor in self.donors:
            yield donor

    def __eq__(self, other):
        """ Returns whether this donor list has all the
        same donors as the other donor list.
        Args:
            other (DonorList) : DonorList to compare
        Returns:
            bool : True if both lists share donors, False otherwise
        """
        return list(self) == list(other)

    def __lt__(self, other):
        """ Returns whether this donor list evaluates to
        less than the other donor list.
        Args:
            other (DonorList) : DonorList to compare
        Returns:
            bool : True if this list is less than other, False otherwise
        """
        return list(self) < list(other)

    def __str__(self):
        """ Returns this donor list as a string.
        Returns:
            str : donor list as string
        """
        return 'Donors:\n{}'.format(
            '\n'.join([str(donor) for donor in self.donors]))

    def __repr__(self):
        """ Returns representation of this donor list.
        Returns:
            str : representation of donor list
        """
        return 'DonorList({})'.format(
            ', '.join([repr(donor) for donor in self.donors]))

    def write_to(self, outfile):
        """ Writes donor information to given file.
        Args:
            outfile (TextIOWrapper) : open file
        """
        for donor in self:
            outfile.write('{}'.format(donor.name))
            if not donor.donations:
                outfile.write(',None')
            for donation in donor.donations:
                outfile.write(',{:.2f}'.format(donation))
            outfile.write('\n')

    def report(self):
        """ Returns report showing donor names, totals given,
        number of gifts and average gift.
        Returns:
            str : donor report
        """
        report = []
        columns = [
            ('Donor Name', 20, self.name, lambda d: d.name),
            ('Total Given', 12, self.dollar, lambda d: d.total),
            ('Num Gifts', 10, self.number, lambda d: d.num),
            ('Average Gift', 13, self.dollar, lambda d: d.average)]
        headers = '| '.join([
            c + ' ' * (w - len(c)) for c, w, _, _ in columns])
        report.append(headers)
        report_width = sum([c[1] for c in columns]) + (len(columns) - 1) * 2
        report.append('-' * (report_width - 1))
        for donor in self.sort_by('total'):
            row = [
                form(yld(donor), width)
                for (_, width, form, yld) in columns]
            report.append(' '.join(row))
        return '\n'.join(report)

    @staticmethod
    def name(name, width):
        """ Returns name for use in report.
        Args:
            name (str) : name to process
            width (int) : width of column
        Returns:
            str : processed name
        """
        name = name[:width - 4] + '...' if len(name) > width else name
        return name + ' ' * (width - len(name))

    @staticmethod
    def dollar(d, width):
        """ Returns dollar amount for use in report.
        Args:
            d (float) : dollar amount to process
        Returns:
            str : processed dollar amount
        """
        d = '999,999.99+' if d > 999999.99 else '{:,.2f}'.format(d)
        return '${}{}'.format(' ' * (width - len(str(d)) - 1), d)

    @staticmethod
    def number(n, width):
        """ Returns numerical amount for use in report.
        Args:
            n (float) : numerical amount to process
        Returns:
            str : processed numerical amount
        """
        n = '999,999+' if n > 9999999 else'{:,}'.format(n)
        return ' ' * (width + 1 - len(n)) + n + ' '

    def challenge_all(self, factor, min_donation=None, max_donation=None):
        donors = map(lambda d: d.multiply(
            factor, min_donation, max_donation), self.donors)
        return DonorList(*donors)

    def challenge_donor(
            self, name, factor, min_donation=None, max_donation=None):
        return self[name].multiply(factor, min_donation, max_donation)
