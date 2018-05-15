# Copyright (C) 2018 Herman Õunapuu
#
# This file is part of Linux GPU Manager.
#
# Linux GPU Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Linux GPU Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Linux GPU Manager.  If not, see <http://www.gnu.org/licenses/>.


from enum import Enum


class Action(Enum):
    THROTTLE_MODERATE = 1
    THROTTLE_CRITICAL = 2
    BOOST_MODERATE = 3
    BOOST_CRITICAL = 4
    NO_OP = 5
