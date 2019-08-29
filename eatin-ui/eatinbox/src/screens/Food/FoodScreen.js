import React from 'react'
import { 
View,
StyleSheet,
Dimensions,
} from 'react-native';

import LocationHeader from './Header/LocationHeader';
import BrowseHeader from './Header/BrowseHeader';
import Foodlist from './Foodlist';
import EIBHeader from './Header/EIBHeader';
import MealType from './Header/Type';
import { TouchableOpacity } from 'react-native-gesture-handler';

const width = Dimensions.get('window').width

const FoodScreen = (props) => (
    <View style={styles.container}>
        <EIBHeader />
        <LocationHeader/>
        <BrowseHeader/>          
        <MealType />  
        <Foodlist/>
    </View>
);

const styles = StyleSheet.create({
    container: {
        flex:1,
        width,
        alignItems: 'center',
        // backgroundColor: '#e8e8e8',
    },
})

export default FoodScreen;
