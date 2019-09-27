import React from 'react'
import { 
View,
StyleSheet,
Dimensions,
} from 'react-native';

import LocationHeader from './Header/LocationHeader';
import Foodlist from './Foodlist';
import MealType from './Header/TypeMeal';
import Ads from './ADs/Ads';

const width = Dimensions.get('window').width

const FoodScreen = (props) => (
    <View style={styles.container}>
        <LocationHeader/>
        <MealType />  
        <Ads/>
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
